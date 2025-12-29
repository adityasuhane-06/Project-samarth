"""
RAG (Retrieval Augmented Generation) Service using ChromaDB
Enables semantic search over agricultural knowledge base
"""
import os
from typing import List, Dict, Any, Optional
import json

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

from config.settings import settings


# ============================================================================
# CHROMA CLOUD CONFIGURATION
# ============================================================================

# Load from environment variables
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
# Note: Database name has trailing space in Chroma Cloud
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "Project Samarth ")
# Ensure trailing space if not present (Chroma Cloud quirk)
if CHROMA_DATABASE and not CHROMA_DATABASE.endswith(" "):
    CHROMA_DATABASE = CHROMA_DATABASE + " "


# ============================================================================
# AGRICULTURAL KNOWLEDGE BASE
# ===================================================================================================================================================

AGRICULTURAL_KNOWLEDGE = [
    # Data source descriptions
    {
        "content": "APEDA (Agricultural and Processed Food Products Export Development Authority) provides state-level export data for agricultural products from 2019 to 2024. Categories include Agri (cereals, grains), Fruits, Vegetables, Spices, LiveStock, Plantations, and Floriculture.",
        "metadata": {"source": "data_sources", "type": "apeda", "years": "2019-2024"}
    },
    {
        "content": "District-level crop production data covers years 2013 to 2015. This dataset includes production quantities, area cultivated, and yield for major crops across all Indian districts.",
        "metadata": {"source": "data_sources", "type": "crop_production", "years": "2013-2015"}
    },
    {
        "content": "Daily rainfall data is available at district level from 2019 to 2024. This includes daily precipitation measurements useful for recent weather pattern analysis.",
        "metadata": {"source": "data_sources", "type": "daily_rainfall", "years": "2019-2024"}
    },
    {
        "content": "Historical rainfall data spans from 1901 to 2015 at the state level. Includes monthly, seasonal, and annual rainfall totals. Ideal for long-term climate trend analysis.",
        "metadata": {"source": "data_sources", "type": "historical_rainfall", "years": "1901-2015"}
    },
    
    # Crop information - Major Food Grains
    {
        "content": "Rice is India's primary food grain crop, grown extensively in states like West Bengal, Uttar Pradesh, Punjab, and Tamil Nadu. Kharif crop requiring 100-200cm rainfall. India is the world's second-largest rice producer after China.",
        "metadata": {"source": "crop_info", "crop": "rice", "season": "kharif", "category": "food_grain"}
    },
    {
        "content": "Wheat is the second most important food grain in India, primarily grown in Punjab, Haryana, Uttar Pradesh, and Madhya Pradesh. Rabi crop requiring cool climate with 50-75cm rainfall. India is the world's second-largest wheat producer.",
        "metadata": {"source": "crop_info", "crop": "wheat", "season": "rabi", "category": "food_grain"}
    },
    {
        "content": "Maize (corn) is grown in Karnataka, Madhya Pradesh, Bihar, and Andhra Pradesh. Can be grown in both Kharif and Rabi seasons. Requires moderate rainfall of 50-75cm. Important for poultry feed and food processing.",
        "metadata": {"source": "crop_info", "crop": "maize", "season": "both", "category": "food_grain"}
    },
    {
        "content": "Bajra (pearl millet) is a drought-resistant crop grown in Rajasthan, Maharashtra, Gujarat, and Haryana. Kharif crop requiring minimal rainfall (40-50cm). Important for food security in arid regions.",
        "metadata": {"source": "crop_info", "crop": "bajra", "season": "kharif", "category": "food_grain"}
    },
    {
        "content": "Jowar (sorghum) is grown in Maharashtra, Karnataka, and Madhya Pradesh. Drought-resistant Kharif crop requiring 40-60cm rainfall. Used for food and fodder.",
        "metadata": {"source": "crop_info", "crop": "jowar", "season": "kharif", "category": "food_grain"}
    },
    
    # Pulses
    {
        "content": "Pulses including lentils, chickpeas, and beans are protein-rich crops grown across Madhya Pradesh, Maharashtra, Rajasthan. Important for soil nitrogen fixation. India is the largest producer and consumer of pulses globally.",
        "metadata": {"source": "crop_info", "crop": "pulses", "season": "rabi", "category": "pulses"}
    },
    {
        "content": "Chickpea (chana) is the most important pulse crop in India, grown in Madhya Pradesh, Rajasthan, and Maharashtra. Rabi crop requiring cool, dry climate with 60-90cm annual rainfall.",
        "metadata": {"source": "crop_info", "crop": "chickpea", "season": "rabi", "category": "pulses"}
    },
    {
        "content": "Pigeon pea (tur/arhar) is a major pulse grown in Maharashtra, Karnataka, and Madhya Pradesh. Kharif crop requiring 60-65cm rainfall. Takes 6-9 months to mature.",
        "metadata": {"source": "crop_info", "crop": "pigeon_pea", "season": "kharif", "category": "pulses"}
    },
    {
        "content": "Black gram (urad) and green gram (moong) are short-duration pulses grown across India. Both Kharif and Rabi crops. Rich in protein and important for crop rotation.",
        "metadata": {"source": "crop_info", "crop": "black_gram_green_gram", "season": "both", "category": "pulses"}
    },
    
    # Cash Crops
    {
        "content": "Cotton is a major cash crop grown in Maharashtra, Gujarat, Andhra Pradesh, and Punjab. Requires warm climate with moderate rainfall of 50-100cm. India is the world's largest cotton producer.",
        "metadata": {"source": "crop_info", "crop": "cotton", "season": "kharif", "category": "cash_crop"}
    },
    {
        "content": "Sugarcane is grown in Uttar Pradesh, Maharashtra, Karnataka, and Tamil Nadu. Requires hot and humid climate with 75-150cm rainfall and good irrigation. India is the world's second-largest sugarcane producer.",
        "metadata": {"source": "crop_info", "crop": "sugarcane", "season": "annual", "category": "cash_crop"}
    },
    {
        "content": "Jute is a fiber crop known as 'golden fiber', primarily grown in West Bengal and Bihar. Requires hot and humid climate with heavy rainfall (150-200cm). India is the world's largest jute producer.",
        "metadata": {"source": "crop_info", "crop": "jute", "season": "kharif", "category": "cash_crop"}
    },
    {
        "content": "Tea is grown in Assam, West Bengal, Tamil Nadu, and Kerala. Requires tropical/subtropical climate with high humidity and 150-300cm rainfall. India is the world's second-largest tea producer.",
        "metadata": {"source": "crop_info", "crop": "tea", "season": "annual", "category": "plantation"}
    },
    {
        "content": "Coffee is grown in Karnataka, Kerala, and Tamil Nadu, primarily in hilly regions. Requires tropical climate with moderate rainfall (150-200cm) and shade. India produces both Arabica and Robusta varieties.",
        "metadata": {"source": "crop_info", "crop": "coffee", "season": "annual", "category": "plantation"}
    },
    {
        "content": "Rubber is grown in Kerala, Tamil Nadu, and Karnataka. Requires hot, humid climate with high rainfall (200-300cm). India is the sixth-largest natural rubber producer globally.",
        "metadata": {"source": "crop_info", "crop": "rubber", "season": "annual", "category": "plantation"}
    },
    {
        "content": "Tobacco is grown in Andhra Pradesh, Gujarat, and Karnataka. Kharif crop requiring moderate rainfall (75-100cm). Used for cigarettes, bidis, and chewing tobacco.",
        "metadata": {"source": "crop_info", "crop": "tobacco", "season": "kharif", "category": "cash_crop"}
    },
    
    # Oilseeds
    {
        "content": "Groundnut (peanut) is a major oilseed crop grown in Gujarat, Andhra Pradesh, and Tamil Nadu. Kharif crop requiring 50-75cm rainfall. Rich in protein and oil content.",
        "metadata": {"source": "crop_info", "crop": "groundnut", "season": "kharif", "category": "oilseed"}
    },
    {
        "content": "Mustard and rapeseed are important Rabi oilseed crops grown in Rajasthan, Uttar Pradesh, and Haryana. Require cool climate with 40-50cm rainfall.",
        "metadata": {"source": "crop_info", "crop": "mustard", "season": "rabi", "category": "oilseed"}
    },
    {
        "content": "Sunflower is grown in Karnataka, Maharashtra, and Andhra Pradesh. Can be cultivated in both Kharif and Rabi seasons. Requires moderate rainfall of 50-75cm.",
        "metadata": {"source": "crop_info", "crop": "sunflower", "season": "both", "category": "oilseed"}
    },
    {
        "content": "Soybean is a major oilseed and protein crop grown in Madhya Pradesh, Maharashtra, and Rajasthan. Kharif crop requiring 60-80cm rainfall. Important for oil extraction and protein meal.",
        "metadata": {"source": "crop_info", "crop": "soybean", "season": "kharif", "category": "oilseed"}
    },
    {
        "content": "Coconut is grown extensively in Kerala, Karnataka, and Tamil Nadu. Requires tropical climate with 150-250cm annual rainfall. India is the third-largest coconut producer globally.",
        "metadata": {"source": "crop_info", "crop": "coconut", "season": "annual", "category": "plantation"}
    },
    
    # Spices
    {
        "content": "Black pepper is known as the 'King of Spices', grown in Kerala, Karnataka, and Tamil Nadu. Requires hot, humid climate with heavy rainfall (200-300cm). India is the largest consumer of black pepper.",
        "metadata": {"source": "crop_info", "crop": "black_pepper", "season": "annual", "category": "spice"}
    },
    {
        "content": "Cardamom is the 'Queen of Spices', cultivated in Kerala, Karnataka, and Tamil Nadu. Requires cool, humid climate with 150-400cm rainfall. India is the world's largest cardamom producer.",
        "metadata": {"source": "crop_info", "crop": "cardamom", "season": "annual", "category": "spice"}
    },
    {
        "content": "Turmeric is grown in Telangana, Maharashtra, and Tamil Nadu. Requires warm, humid climate with 150-200cm rainfall. India produces 80% of the world's turmeric.",
        "metadata": {"source": "crop_info", "crop": "turmeric", "season": "kharif", "category": "spice"}
    },
    {
        "content": "Chilli is grown extensively in Andhra Pradesh, Telangana, and Karnataka. Requires warm climate with moderate rainfall (60-100cm). India is the largest producer, consumer, and exporter of chilli.",
        "metadata": {"source": "crop_info", "crop": "chilli", "season": "both", "category": "spice"}
    },
    {
        "content": "Ginger is cultivated in Kerala, Meghalaya, and Arunachal Pradesh. Requires warm, humid climate with 150-300cm rainfall. Used both as spice and for medicinal purposes.",
        "metadata": {"source": "crop_info", "crop": "ginger", "season": "kharif", "category": "spice"}
    },
    
    # Fruits
    {
        "content": "Mango is the 'King of Fruits' in India, grown in Uttar Pradesh, Andhra Pradesh, Karnataka, and Bihar. Requires tropical/subtropical climate. India is the world's largest mango producer.",
        "metadata": {"source": "crop_info", "crop": "mango", "season": "annual", "category": "fruit"}
    },
    {
        "content": "Banana is grown throughout India, especially in Tamil Nadu, Maharashtra, and Gujarat. Requires hot, humid climate with regular irrigation. India is the largest banana producer globally.",
        "metadata": {"source": "crop_info", "crop": "banana", "season": "annual", "category": "fruit"}
    },
    {
        "content": "Citrus fruits including oranges, lemons, and sweet lime are grown in Maharashtra, Madhya Pradesh, and Andhra Pradesh. Require subtropical climate with moderate rainfall.",
        "metadata": {"source": "crop_info", "crop": "citrus", "season": "annual", "category": "fruit"}
    },
    {
        "content": "Grapes are grown in Maharashtra, Karnataka, and Andhra Pradesh. Require warm, dry climate with controlled irrigation. Important for fresh consumption, raisins, and wine production.",
        "metadata": {"source": "crop_info", "crop": "grapes", "season": "annual", "category": "fruit"}
    },
    {
        "content": "Apple cultivation is concentrated in Himachal Pradesh, Jammu & Kashmir, and Uttarakhand. Requires temperate climate with cold winters and moderate summers.",
        "metadata": {"source": "crop_info", "crop": "apple", "season": "annual", "category": "fruit"}
    },
    
    # Vegetables
    {
        "content": "Potato is the most important vegetable crop grown in Uttar Pradesh, West Bengal, Bihar, and Punjab. Rabi crop requiring cool climate with 50-75cm rainfall.",
        "metadata": {"source": "crop_info", "crop": "potato", "season": "rabi", "category": "vegetable"}
    },
    {
        "content": "Onion is grown in Maharashtra, Karnataka, and Madhya Pradesh. Can be cultivated in both Kharif and Rabi seasons. Requires moderate rainfall and cool climate for bulb formation.",
        "metadata": {"source": "crop_info", "crop": "onion", "season": "both", "category": "vegetable"}
    },
    {
        "content": "Tomato is grown throughout India, with major production in Andhra Pradesh, Karnataka, and Maharashtra. Requires warm climate with moderate rainfall (60-100cm).",
        "metadata": {"source": "crop_info", "crop": "tomato", "season": "both", "category": "vegetable"}
    },
    
    # Regional information - Detailed
    {
        "content": "Punjab is known as the 'Granary of India' and 'Bread Basket of India' due to its high wheat and rice production. Uses extensive canal irrigation from Sutlej, Beas, and Ravi rivers. Contributes significantly to India's food grain reserves.",
        "metadata": {"source": "regional_info", "state": "Punjab", "specialty": "wheat, rice", "nickname": "Granary of India"}
    },
    {
        "content": "Haryana is a major producer of wheat, rice, sugarcane, and oilseeds. Well-developed irrigation infrastructure. Part of the Green Revolution success story along with Punjab.",
        "metadata": {"source": "regional_info", "state": "Haryana", "specialty": "wheat, rice", "irrigation": "high"}
    },
    {
        "content": "Uttar Pradesh is India's largest producer of wheat, sugarcane, and potatoes. The Gangetic plains provide fertile alluvial soil. Also significant rice and pulse production.",
        "metadata": {"source": "regional_info", "state": "Uttar Pradesh", "specialty": "wheat, sugarcane, potato"}
    },
    {
        "content": "Madhya Pradesh is the largest producer of pulses and soybean in India. Also significant wheat, rice, and oilseed production. Known as the 'Soybean state of India'.",
        "metadata": {"source": "regional_info", "state": "Madhya Pradesh", "specialty": "pulses, soybean", "nickname": "Soybean state"}
    },
    {
        "content": "Maharashtra is the largest producer of sugarcane, grapes, mangoes, and cotton. Also significant onion and soybean production. Diverse agro-climatic zones support varied crops.",
        "metadata": {"source": "regional_info", "state": "Maharashtra", "specialty": "sugarcane, fruits, cotton"}
    },
    {
        "content": "Gujarat is a major producer of cotton, groundnut, and tobacco. Also significant production of cumin, fennel, and other spices. Well-developed dairy sector.",
        "metadata": {"source": "regional_info", "state": "Gujarat", "specialty": "cotton, groundnut, dairy"}
    },
    {
        "content": "Rajasthan is the largest producer of bajra (pearl millet) and mustard in India. Also significant production of pulses and spices. Agriculture adapted to arid climate.",
        "metadata": {"source": "regional_info", "state": "Rajasthan", "specialty": "bajra, mustard", "climate": "arid"}
    },
    {
        "content": "West Bengal is a major producer of rice and jute. The Gangetic delta provides highly fertile soil. Also significant vegetable and fish production.",
        "metadata": {"source": "regional_info", "state": "West Bengal", "specialty": "rice, jute, fish"}
    },
    {
        "content": "Bihar is a significant producer of rice, wheat, maize, and pulses. The fertile Gangetic plains support intensive agriculture. Also important for vegetable production.",
        "metadata": {"source": "regional_info", "state": "Bihar", "specialty": "rice, wheat, vegetables"}
    },
    {
        "content": "Karnataka is a major producer of coffee, silk, and spices. Also significant production of ragi (finger millet), rice, and sugarcane. Diverse agro-climatic zones.",
        "metadata": {"source": "regional_info", "state": "Karnataka", "specialty": "coffee, silk, spices"}
    },
    {
        "content": "Tamil Nadu is a major producer of rice, sugarcane, and groundnut. Also significant production of cotton, turmeric, and bananas. Well-developed irrigation from Cauvery river.",
        "metadata": {"source": "regional_info", "state": "Tamil Nadu", "specialty": "rice, sugarcane, groundnut"}
    },
    {
        "content": "Kerala is famous for spices (pepper, cardamom), coconut, rubber, and tea plantations. Receives heavy monsoon rainfall. High literacy and HDI but limited agricultural land.",
        "metadata": {"source": "regional_info", "state": "Kerala", "specialty": "spices, coconut, rubber, tea"}
    },
    {
        "content": "Andhra Pradesh and Telangana are major producers of rice, chillies, tobacco, and turmeric. Krishna and Godavari river deltas are highly fertile. Important for aquaculture as well.",
        "metadata": {"source": "regional_info", "state": "Andhra Pradesh", "specialty": "rice, chillies, turmeric"}
    },
    {
        "content": "Assam is the largest producer of tea in India, accounting for over 50% of national production. Also produces rice, jute, and bamboo. High rainfall region.",
        "metadata": {"source": "regional_info", "state": "Assam", "specialty": "tea, rice", "rainfall": "high"}
    },
    
    # Agricultural Seasons
    {
        "content": "Kharif season crops are sown with the onset of monsoon (June-July) and harvested in September-October. Major crops include rice, cotton, bajra, jowar, maize, and pulses. Depends on southwest monsoon.",
        "metadata": {"source": "season_info", "season": "kharif", "months": "June-October"}
    },
    {
        "content": "Rabi season crops are sown in October-November and harvested in March-April. Major crops include wheat, gram, mustard, barley, and peas. Depends on winter rainfall and irrigation.",
        "metadata": {"source": "season_info", "season": "rabi", "months": "October-April"}
    },
    {
        "content": "Zaid season is a short summer season between Rabi and Kharif (March-June). Crops include watermelon, muskmelon, cucumber, and vegetables. Requires irrigation.",
        "metadata": {"source": "season_info", "season": "zaid", "months": "March-June"}
    },
    
    # Soil Types
    {
        "content": "Alluvial soil is the most widespread and fertile soil type in India, covering the Indo-Gangetic plains. Rich in potash but poor in phosphorus. Ideal for rice, wheat, sugarcane, and pulses.",
        "metadata": {"source": "soil_info", "soil_type": "alluvial", "crops": "rice, wheat, sugarcane"}
    },
    {
        "content": "Black soil (Regur) is rich in clay, calcium, and magnesium. Found in Maharashtra, Madhya Pradesh, Gujarat, and parts of Andhra Pradesh. Ideal for cotton cultivation, hence called 'black cotton soil'.",
        "metadata": {"source": "soil_info", "soil_type": "black", "crops": "cotton, jowar, wheat"}
    },
    {
        "content": "Red soil is found in Tamil Nadu, Karnataka, and parts of Maharashtra. Formed by weathering of ancient crystalline rocks. Suitable for millets, groundnut, and pulses.",
        "metadata": {"source": "soil_info", "soil_type": "red", "crops": "millets, groundnut, pulses"}
    },
    {
        "content": "Laterite soil is found in high rainfall areas of Western Ghats, Eastern Ghats, and hills of northeastern India. Rich in iron and aluminum but poor in nitrogen and phosphorus. Suitable for cashew, rubber, and tea.",
        "metadata": {"source": "soil_info", "soil_type": "laterite", "crops": "cashew, rubber, tea"}
    },
    {
        "content": "Desert soil is found in Rajasthan and parts of Gujarat. Sandy texture with low water retention. Suitable for drought-resistant crops like bajra, jowar, and pulses with irrigation.",
        "metadata": {"source": "soil_info", "soil_type": "desert", "crops": "bajra, pulses"}
    },
    
    # Irrigation
    {
        "content": "Canal irrigation is the most important source of irrigation in India, covering states like Punjab, Haryana, and Uttar Pradesh. Fed by perennial rivers like Indus, Ganga, and Brahmaputra.",
        "metadata": {"source": "irrigation_info", "type": "canal", "coverage": "high"}
    },
    {
        "content": "Well and tube-well irrigation covers the largest irrigated area in India. Important in Punjab, Haryana, Uttar Pradesh, and parts of South India. Uses groundwater resources.",
        "metadata": {"source": "irrigation_info", "type": "well_tubewell", "coverage": "highest"}
    },
    {
        "content": "Tank irrigation is traditional in South India, especially Tamil Nadu, Karnataka, and Andhra Pradesh. Small reservoirs store rainwater for irrigation. Ancient system but declining importance.",
        "metadata": {"source": "irrigation_info", "type": "tank", "region": "South India"}
    },
    {
        "content": "Drip and sprinkler irrigation are modern methods gaining popularity. Water-efficient systems suitable for water-scarce regions. Government provides subsidies for adoption.",
        "metadata": {"source": "irrigation_info", "type": "drip_sprinkler", "efficiency": "high"}
    },
    
    # System capabilities
    {
        "content": "Project Samarth uses a two-model architecture: QueryRouter for intelligent dataset selection and QueryProcessor for answer generation. Both use Google Gemini 2.5-flash for fast, accurate responses.",
        "metadata": {"source": "system_info", "type": "architecture"}
    },
    {
        "content": "The system integrates 5 government data sources covering agricultural production, exports, and rainfall from 1901 to 2024, spanning over 120 years of historical data.",
        "metadata": {"source": "system_info", "type": "data_coverage"}
    },
    {
        "content": "MongoDB caching reduces response time from 13 seconds to 0.1 seconds (130x improvement) by storing query results with smart TTL-based expiration. Improves user experience significantly.",
        "metadata": {"source": "system_info", "type": "caching"}
    },
    {
        "content": "RAG (Retrieval Augmented Generation) service uses ChromaDB vector database and HuggingFace embeddings for semantic search. Provides context-aware answers to agricultural queries.",
        "metadata": {"source": "system_info", "type": "rag"}
    },
    {
        "content": "FastAPI backend provides RESTful endpoints for querying agricultural data. Supports data export in CSV and JSON formats. Built for scalability and performance.",
        "metadata": {"source": "system_info", "type": "backend"}
    },
    
    # Government Schemes
    {
        "content": "Pradhan Mantri Fasal Bima Yojana (PMFBY) is a crop insurance scheme protecting farmers against crop loss due to natural calamities, pests, and diseases. Launched in 2016.",
        "metadata": {"source": "scheme_info", "scheme": "PMFBY", "year": "2016", "type": "insurance"}
    },
    {
        "content": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) provides income support of ₹6000 per year to all farmer families. Direct benefit transfer in three installments. Launched in 2019.",
        "metadata": {"source": "scheme_info", "scheme": "PM-KISAN", "year": "2019", "type": "income_support"}
    },
    {
        "content": "Soil Health Card Scheme provides soil nutrient status information to farmers. Helps in balanced fertilizer application. Issued every 2-3 years to all farmers.",
        "metadata": {"source": "scheme_info", "scheme": "Soil Health Card", "type": "advisory"}
    },
    {
        "content": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY) aims to expand irrigated area and improve water use efficiency. Focus on 'per drop more crop'. Promotes micro-irrigation.",
        "metadata": {"source": "scheme_info", "scheme": "PMKSY", "type": "irrigation"}
    },
    
    # Crop Water Requirements
    {
        "content": "Low water requirement crops include bajra (pearl millet), jowar (sorghum), ragi (finger millet), chickpea, and groundnut. These crops need 350-650mm annual rainfall and are ideal for drought-prone regions and water-scarce areas.",
        "metadata": {"source": "water_info", "water_need": "low", "rainfall": "350-650mm"}
    },
    {
        "content": "Medium water requirement crops include wheat, maize, cotton, soybean, and sunflower. These crops need 500-900mm annual rainfall and moderate irrigation. Suitable for regions with limited irrigation facilities.",
        "metadata": {"source": "water_info", "water_need": "medium", "rainfall": "500-900mm"}
    },
    {
        "content": "High water requirement crops include rice, sugarcane, banana, and jute. Rice needs 1000-2000mm water, sugarcane needs 1500-2500mm. These crops require assured irrigation or high rainfall regions.",
        "metadata": {"source": "water_info", "water_need": "high", "rainfall": "1000-2500mm"}
    },
    {
        "content": "Millets (bajra, jowar, ragi) are the most water-efficient crops, requiring 3-4 times less water than rice. They are climate-resilient, drought-tolerant, and nutritionally superior. Government is promoting millets as 'Shree Anna' (super grains).",
        "metadata": {"source": "water_info", "crop_type": "millets", "efficiency": "very_high"}
    },
    {
        "content": "Pulses are water-efficient legumes requiring 400-700mm rainfall. They fix atmospheric nitrogen, reducing fertilizer needs. Include chickpea, pigeon pea, lentils, and green gram. Important for sustainable agriculture.",
        "metadata": {"source": "water_info", "crop_type": "pulses", "efficiency": "high", "nitrogen_fixing": "yes"}
    },
    
    # High Demand Crops - Food Security
    {
        "content": "Rice is India's most in-demand food grain, consumed by over 65% of the population as staple food. Demand remains consistently high with annual production around 130 million tonnes. Essential for food security.",
        "metadata": {"source": "demand_info", "crop": "rice", "demand_level": "very_high", "category": "food_security"}
    },
    {
        "content": "Wheat is the second most demanded food grain in India, especially in North India. Annual production around 110 million tonnes. Critical for government food distribution programs and public welfare schemes.",
        "metadata": {"source": "demand_info", "crop": "wheat", "demand_level": "very_high", "category": "food_security"}
    },
    {
        "content": "Pulses have high domestic demand but production shortfall leads to imports. Growing health awareness is increasing demand for protein-rich pulses like chickpea, pigeon pea, and lentils. India imports 2-3 million tonnes annually.",
        "metadata": {"source": "demand_info", "crop": "pulses", "demand_level": "high", "demand_gap": "yes"}
    },
    {
        "content": "Edible oils have massive demand-supply gap with 60-70% import dependency. Oilseeds like soybean, groundnut, mustard, and sunflower are in high demand. Government promoting oilseed production to reduce imports.",
        "metadata": {"source": "demand_info", "crop": "oilseeds", "demand_level": "very_high", "import_dependency": "high"}
    },
    
    # High Demand Crops - Commercial
    {
        "content": "Cotton has high domestic and export demand. India is world's largest cotton producer and second-largest exporter. Textile industry depends on cotton supply. Annual production around 35 million bales.",
        "metadata": {"source": "demand_info", "crop": "cotton", "demand_level": "high", "category": "export"}
    },
    {
        "content": "Sugarcane has consistent high demand for sugar production. India is world's second-largest sugar producer. Ethanol blending program is increasing demand further. Farmers prefer sugarcane due to assured prices.",
        "metadata": {"source": "demand_info", "crop": "sugarcane", "demand_level": "high", "category": "industrial"}
    },
    {
        "content": "Spices (turmeric, chilli, black pepper, cardamom) have strong domestic and export demand. India is the world's largest spice producer, consumer, and exporter. Growing global demand for Indian spices.",
        "metadata": {"source": "demand_info", "crop": "spices", "demand_level": "high", "category": "export"}
    },
    {
        "content": "Organic fruits and vegetables have rapidly growing demand due to health consciousness. Premium prices in urban markets. Export opportunities to developed countries. Government promoting organic farming.",
        "metadata": {"source": "demand_info", "crop": "organic_produce", "demand_level": "high", "growth": "rapid"}
    },
    {
        "content": "Horticulture crops (fruits and vegetables) have increasing demand from processing industry and exports. Mango, banana, potato, onion, tomato see consistent high demand. Cold storage and supply chain improvements boosting production.",
        "metadata": {"source": "demand_info", "crop": "horticulture", "demand_level": "high", "category": "processing"}
    },
    {
        "content": "Millets are experiencing demand surge due to health benefits, climate resilience, and government promotion. Declared 'International Year of Millets 2023' by UN. Export demand growing rapidly.",
        "metadata": {"source": "demand_info", "crop": "millets", "demand_level": "growing", "trend": "upward"}
    },
    
    # Detailed Kharif Season Information
    {
        "content": "Kharif rice cultivation begins with monsoon onset in June-July. Transplanting done after adequate rainfall. Requires standing water and warm temperatures (25-35°C). Harvested in October-November. Major producing states: West Bengal, Uttar Pradesh, Punjab.",
        "metadata": {"source": "kharif_crops", "crop": "rice", "sowing": "June-July", "harvesting": "October-November"}
    },
    {
        "content": "Kharif cotton is sown in May-June in rainfed areas and June-July in irrigated areas. Requires 180-200 days to mature. Needs warm, moist conditions during growth and dry weather during picking. Harvested in October-January.",
        "metadata": {"source": "kharif_crops", "crop": "cotton", "sowing": "May-July", "harvesting": "October-January"}
    },
    {
        "content": "Kharif bajra (pearl millet) is sown in June-July with early monsoon. Drought-resistant crop maturing in 70-90 days. Can grow in low rainfall areas (400-600mm). Harvested in September-October. Ideal for arid regions.",
        "metadata": {"source": "kharif_crops", "crop": "bajra", "sowing": "June-July", "harvesting": "September-October", "drought_resistant": "yes"}
    },
    {
        "content": "Kharif jowar (sorghum) is sown in June-July. Drought-tolerant crop requiring 450-600mm rainfall. Matures in 90-120 days. Used for food and fodder. Harvested in September-October. Important for dryland agriculture.",
        "metadata": {"source": "kharif_crops", "crop": "jowar", "sowing": "June-July", "harvesting": "September-October", "drought_tolerant": "yes"}
    },
    {
        "content": "Kharif maize is sown in June-July with monsoon. Versatile crop used for food, feed, and industry. Requires 500-750mm rainfall. Matures in 90-110 days. Harvested in September-October.",
        "metadata": {"source": "kharif_crops", "crop": "maize", "sowing": "June-July", "harvesting": "September-October"}
    },
    {
        "content": "Kharif groundnut is sown in June-July. Requires warm climate with 500-750mm rainfall. Matures in 120-140 days. Important oilseed crop. Harvested in October-November. Fixes nitrogen in soil.",
        "metadata": {"source": "kharif_crops", "crop": "groundnut", "sowing": "June-July", "harvesting": "October-November"}
    },
    {
        "content": "Kharif soybean is sown in June-July at monsoon onset. Requires 600-800mm rainfall. Matures in 90-120 days. Major oilseed crop with protein-rich meal. Harvested in September-October. Madhya Pradesh is largest producer.",
        "metadata": {"source": "kharif_crops", "crop": "soybean", "sowing": "June-July", "harvesting": "September-October"}
    },
    {
        "content": "Kharif pigeon pea (tur/arhar) is sown in June-July. Long duration crop taking 180-240 days. Drought-tolerant after establishment. Important pulse crop. Harvested in December-January.",
        "metadata": {"source": "kharif_crops", "crop": "pigeon_pea", "sowing": "June-July", "harvesting": "December-January", "duration": "long"}
    },
    
    # Detailed Rabi Season Information
    {
        "content": "Rabi wheat is sown in October-November after monsoon withdrawal. Requires cool growing season and warm ripening period. Needs 450-600mm rainfall/irrigation. Harvested in March-April. Major crop of Punjab, Haryana, UP.",
        "metadata": {"source": "rabi_crops", "crop": "wheat", "sowing": "October-November", "harvesting": "March-April"}
    },
    {
        "content": "Rabi chickpea (chana) is sown in October-November. Requires cool, dry climate. Drought-tolerant crop needing 600-900mm rainfall. Matures in 120-150 days. Harvested in February-March. Major pulse crop of India.",
        "metadata": {"source": "rabi_crops", "crop": "chickpea", "sowing": "October-November", "harvesting": "February-March"}
    },
    {
        "content": "Rabi mustard is sown in October-November. Requires cool weather during growth. Important oilseed crop of North India. Matures in 120-140 days. Harvested in February-March. Rajasthan is largest producer.",
        "metadata": {"source": "rabi_crops", "crop": "mustard", "sowing": "October-November", "harvesting": "February-March"}
    },
    {
        "content": "Rabi barley is sown in October-November. Tolerates saline and alkaline soils better than wheat. Requires 400-500mm water. Matures in 120-140 days. Used for food, feed, and brewing. Harvested in March-April.",
        "metadata": {"source": "rabi_crops", "crop": "barley", "sowing": "October-November", "harvesting": "March-April"}
    },
    {
        "content": "Rabi potato is sown in October-November in plains. Short duration crop maturing in 90-120 days. Requires cool weather and adequate irrigation. Harvested in January-March. Most important vegetable crop of India.",
        "metadata": {"source": "rabi_crops", "crop": "potato", "sowing": "October-November", "harvesting": "January-March"}
    },
    {
        "content": "Rabi onion is sown in November-December. Requires cool season for vegetative growth and warm season for bulb formation. Matures in 120-150 days. Harvested in March-April. Important export crop.",
        "metadata": {"source": "rabi_crops", "crop": "onion", "sowing": "November-December", "harvesting": "March-April"}
    },
    {
        "content": "Rabi lentil (masoor) is sown in October-November. Requires cool, dry climate. Short duration pulse maturing in 100-120 days. Fixes atmospheric nitrogen. Harvested in February-March.",
        "metadata": {"source": "rabi_crops", "crop": "lentil", "sowing": "October-November", "harvesting": "February-March", "nitrogen_fixing": "yes"}
    },
    {
        "content": "Rabi pea is sown in October-November. Requires cool climate. Used as vegetable (green peas) and pulse (dry peas). Matures in 90-120 days. Harvested in January-March. Good for crop rotation.",
        "metadata": {"source": "rabi_crops", "crop": "pea", "sowing": "October-November", "harvesting": "January-March"}
    },
    
    # Zaid Season Details
    {
        "content": "Zaid watermelon is sown in February-March. Short duration crop maturing in 80-90 days. Requires warm weather and irrigation. Harvested in May-June. High demand during summer months.",
        "metadata": {"source": "zaid_crops", "crop": "watermelon", "sowing": "February-March", "harvesting": "May-June"}
    },
    {
        "content": "Zaid muskmelon and cucumber are sown in February-March. Require warm climate and assured irrigation. Mature in 60-90 days. Harvested in May-June. Important summer vegetables with good market demand.",
        "metadata": {"source": "zaid_crops", "crop": "muskmelon_cucumber", "sowing": "February-March", "harvesting": "May-June"}
    },
    {
        "content": "Zaid summer moong (green gram) is sown in March-April. Short duration pulse maturing in 60-70 days. Requires irrigation. Harvested in May-June. Helps in maintaining soil fertility between main crops.",
        "metadata": {"source": "zaid_crops", "crop": "moong", "sowing": "March-April", "harvesting": "May-June", "duration": "short"}
    },
    {
        "content": "Zaid fodder crops (jowar, maize) are grown in February-April for cattle feed during summer. Require irrigation. Harvested in 60-80 days. Important for dairy farming and livestock maintenance.",
        "metadata": {"source": "zaid_crops", "crop": "fodder", "sowing": "February-April", "harvesting": "April-June", "purpose": "livestock"}
    },
    
    # Perennial/Annual Crops
    {
        "content": "Sugarcane is a long-duration perennial crop planted in February-March (spring) or October-November (autumn). Takes 10-18 months to mature. Requires continuous irrigation. Harvested in phases from November to April.",
        "metadata": {"source": "perennial_crops", "crop": "sugarcane", "duration": "10-18 months", "planting": "February-March or October-November"}
    },
    {
        "content": "Banana is a perennial crop planted throughout the year with irrigation. Takes 11-15 months for first harvest. After that, produces continuously. Requires warm, humid climate with regular irrigation.",
        "metadata": {"source": "perennial_crops", "crop": "banana", "duration": "11-15 months", "type": "continuous"}
    },
    {
        "content": "Papaya is planted in July-August or February-March. Starts fruiting in 9-12 months and continues for 3-4 years. Requires warm climate with good drainage. Year-round fruit production possible.",
        "metadata": {"source": "perennial_crops", "crop": "papaya", "planting": "July-August or February-March", "fruiting_duration": "3-4 years"}
    },
    
    # Agricultural Challenges
    {
        "content": "Climate change poses significant risks to Indian agriculture including erratic rainfall, rising temperatures, and increased frequency of droughts and floods. Affects crop productivity and farmer incomes.",
        "metadata": {"source": "challenge_info", "challenge": "climate_change", "impact": "high"}
    },
    {
        "content": "Small and fragmented landholdings limit mechanization and economies of scale. Average farm size is around 1.08 hectares. Makes farming economically unviable for many farmers.",
        "metadata": {"source": "challenge_info", "challenge": "land_fragmentation", "impact": "high"}
    },
    {
        "content": "Water scarcity and declining groundwater levels affect agricultural sustainability. Over-exploitation of groundwater in Punjab, Haryana, and parts of Rajasthan. Need for water conservation.",
        "metadata": {"source": "challenge_info", "challenge": "water_scarcity", "impact": "high"}
    },
    {
        "content": "Soil degradation from excessive fertilizer use, monoculture, and lack of organic matter reduces soil fertility. Affects long-term agricultural productivity.",
        "metadata": {"source": "challenge_info", "challenge": "soil_degradation", "impact": "medium"}
    },
    {
        "content": "Price volatility and market access challenges affect farmer incomes. Need for better market infrastructure, storage facilities, and price stabilization mechanisms.",
        "metadata": {"source": "challenge_info", "challenge": "market_access", "impact": "high"}
    }
]
# ============================================================================
# RAG SERVICE CLASS
# ============================================================================

class RAGService:
    """
    RAG (Retrieval Augmented Generation) service for agricultural queries
    Uses ChromaDB for vector storage and Google Embeddings
    """
    
    def __init__(self, use_cloud: bool = True):
        """
        Initialize RAG service
        
        Args:
            use_cloud: If True, use Chroma Cloud. If False, use local persistence.
        """
        print("DEBUG: Initializing RAG Service...")
        
        self.use_cloud = use_cloud
        self.collection_name = "agricultural_knowledge"
        
        # Initialize embeddings using HuggingFace (FREE, no API limits!)
        # all-MiniLM-L6-v2 is a fast, efficient embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize LLM for generation
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )
        
        # Initialize Chroma client
        if use_cloud:
            self._init_cloud_client()
        else:
            self._init_local_client()
        
        # Initialize vector store
        self._init_vector_store()
        
        print("DEBUG: RAG Service initialized successfully!")
    
    def _init_cloud_client(self):
        """Initialize Chroma Cloud client"""
        try:
            self.chroma_client = chromadb.CloudClient(
                api_key=CHROMA_API_KEY,
                tenant=CHROMA_TENANT,
                database=CHROMA_DATABASE
            )
            print("DEBUG: Connected to Chroma Cloud")
        except Exception as e:
            print(f"DEBUG: Chroma Cloud connection failed: {e}, falling back to local")
            self._init_local_client()
            self.use_cloud = False
    
    def _init_local_client(self):
        """Initialize local Chroma client with persistence"""
        persist_dir = os.path.join(os.path.dirname(__file__), "..", "..", "chroma_db")
        os.makedirs(persist_dir, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        print(f"DEBUG: Using local Chroma at {persist_dir}")
    
    def _init_vector_store(self):
        """Initialize or load the vector store"""
        try:
            # Try to get existing collection
            collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Agricultural knowledge base for Project Samarth"}
            )
            
            # Check if collection is empty
            count = collection.count()
            print(f"DEBUG: Collection '{self.collection_name}' has {count} documents")
            
            # Create LangChain Chroma wrapper
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            
            # Populate if empty
            if count == 0:
                print("DEBUG: Populating knowledge base...")
                self._populate_knowledge_base()
                
        except Exception as e:
            print(f"DEBUG: Vector store init error: {e}")
            raise
    
    def _populate_knowledge_base(self):
        """Populate the vector store with agricultural knowledge"""
        documents = []
        
        for item in AGRICULTURAL_KNOWLEDGE:
            doc = Document(
                page_content=item["content"],
                metadata=item["metadata"]
            )
            documents.append(doc)
        
        # Add documents to vector store
        self.vector_store.add_documents(documents)
        print(f"DEBUG: Added {len(documents)} documents to knowledge base")
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents with scores
        """
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": 1 - score  # Convert distance to similarity
                })
            
            return documents
            
        except Exception as e:
            print(f"DEBUG: Search error: {e}")
            return []
    
    def query_with_rag(self, question: str) -> str:
        """
        Answer a question using RAG (Retrieval + Generation)
        
        Args:
            question: User's question
            
        Returns:
            Generated answer with retrieved context
        """
        # Retrieve relevant documents
        relevant_docs = self.search(question, k=3)
        
        if not relevant_docs:
            return "I couldn't find relevant information to answer your question."
        
        # Build context from retrieved documents
        context = "\n\n".join([
            f"[Source: {doc['metadata'].get('source', 'unknown')}]\n{doc['content']}"
            for doc in relevant_docs
        ])
        
        # Create RAG prompt
        rag_prompt = PromptTemplate(
            template="""Use the following context to answer the question. 
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}

Answer:""",
            input_variables=["context", "question"]
        )
        
        # Build and invoke chain
        chain = rag_prompt | self.llm | StrOutputParser()
        
        try:
            answer = chain.invoke({
                "context": context,
                "question": question
            })
            return answer
        except Exception as e:
            print(f"DEBUG: RAG generation error: {e}")
            return f"Error generating answer: {str(e)}"
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None):
        """Add a new document to the knowledge base"""
        doc = Document(
            page_content=content,
            metadata=metadata or {}
        )
        self.vector_store.add_documents([doc])
        print(f"DEBUG: Added document to knowledge base")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "document_count": collection.count(),
                "using_cloud": self.use_cloud
            }
        except Exception as e:
            return {"error": str(e)}


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_rag_service: Optional[RAGService] = None


def get_rag_service(use_cloud: bool = None) -> RAGService:
    """
    Get or create the RAG service singleton
    
    Args:
        use_cloud: If None, auto-detect (use cloud if credentials available)
                   If True, force cloud. If False, force local.
    """
    global _rag_service
    
    if _rag_service is None:
        # Auto-detect: use cloud if credentials are set (for Render deployment)
        if use_cloud is None:
            use_cloud = bool(CHROMA_API_KEY and CHROMA_TENANT)
            if use_cloud:
                print("DEBUG: Chroma Cloud credentials found, using cloud storage")
            else:
                print("DEBUG: No Chroma Cloud credentials, using local storage")
        
        _rag_service = RAGService(use_cloud=use_cloud)
    
    return _rag_service


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def rag_search(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Quick search function"""
    service = get_rag_service()
    return service.search(query, k)


def rag_answer(question: str) -> str:
    """Quick RAG answer function"""
    service = get_rag_service()
    return service.query_with_rag(question)
