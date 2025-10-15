"""
Country and Language Mapping Service
Provides comprehensive country-to-language mapping with ISO codes and multiple language support.
country data from https://github.com/georgique/world-geojson/blob/develop/helper/countryCode.json
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class CountryInfo:
    """Country information with language details"""
    name: str
    code: str  # ISO 3166-1 alpha-2
    primary_language: str
    languages: List[str]  # All supported languages
    region: str  # Geographic region

# Comprehensive country and language mapping using world-geojson data
# Source: https://raw.githubusercontent.com/georgique/world-geojson/refs/heads/develop/helper/countryCode.json
COUNTRY_LANGUAGE_MAP: Dict[str, CountryInfo] = {
    # North America
    "US": CountryInfo("United States", "US", "English", ["English", "Spanish"], "North America"),
    "CA": CountryInfo("Canada", "CA", "English", ["English", "French"], "North America"),
    "MX": CountryInfo("Mexico", "MX", "Spanish", ["Spanish"], "North America"),
    "GT": CountryInfo("Guatemala", "GT", "Spanish", ["Spanish"], "North America"),
    "BZ": CountryInfo("Belize", "BZ", "English", ["English", "Spanish"], "North America"),
    "SV": CountryInfo("El Salvador", "SV", "Spanish", ["Spanish"], "North America"),
    "HN": CountryInfo("Honduras", "HN", "Spanish", ["Spanish"], "North America"),
    "NI": CountryInfo("Nicaragua", "NI", "Spanish", ["Spanish"], "North America"),
    "CR": CountryInfo("Costa Rica", "CR", "Spanish", ["Spanish"], "North America"),
    "PA": CountryInfo("Panama", "PA", "Spanish", ["Spanish"], "North America"),
    "CU": CountryInfo("Cuba", "CU", "Spanish", ["Spanish"], "North America"),
    "JM": CountryInfo("Jamaica", "JM", "English", ["English"], "North America"),
    "HT": CountryInfo("Haiti", "HT", "French", ["French", "Creole"], "North America"),
    "DO": CountryInfo("Dominican Republic", "DO", "Spanish", ["Spanish"], "North America"),
    "PR": CountryInfo("Puerto Rico", "PR", "Spanish", ["Spanish", "English"], "North America"),
    
    # Europe
    "GB": CountryInfo("United Kingdom", "GB", "English", ["English"], "Europe"),
    "IE": CountryInfo("Ireland", "IE", "English", ["English", "Irish"], "Europe"),
    "FR": CountryInfo("France", "FR", "French", ["French"], "Europe"),
    "ES": CountryInfo("Spain", "ES", "Spanish", ["Spanish"], "Europe"),
    "PT": CountryInfo("Portugal", "PT", "Portuguese", ["Portuguese"], "Europe"),
    "IT": CountryInfo("Italy", "IT", "Italian", ["Italian"], "Europe"),
    "DE": CountryInfo("Germany", "DE", "German", ["German"], "Europe"),
    "AT": CountryInfo("Austria", "AT", "German", ["German"], "Europe"),
    "CH": CountryInfo("Switzerland", "CH", "German", ["German", "French", "Italian"], "Europe"),
    "NL": CountryInfo("Netherlands", "NL", "Dutch", ["Dutch", "English"], "Europe"),
    "BE": CountryInfo("Belgium", "BE", "Dutch", ["Dutch", "French", "German"], "Europe"),
    "LU": CountryInfo("Luxembourg", "LU", "Luxembourgish", ["Luxembourgish", "French", "German"], "Europe"),
    "DK": CountryInfo("Denmark", "DK", "Danish", ["Danish", "English"], "Europe"),
    "SE": CountryInfo("Sweden", "SE", "Swedish", ["Swedish", "English"], "Europe"),
    "NO": CountryInfo("Norway", "NO", "Norwegian", ["Norwegian", "English"], "Europe"),
    "FI": CountryInfo("Finland", "FI", "Finnish", ["Finnish", "Swedish", "English"], "Europe"),
    "IS": CountryInfo("Iceland", "IS", "Icelandic", ["Icelandic", "English"], "Europe"),
    "PL": CountryInfo("Poland", "PL", "Polish", ["Polish"], "Europe"),
    "CZ": CountryInfo("Czech Republic", "CZ", "Czech", ["Czech"], "Europe"),
    "SK": CountryInfo("Slovakia", "SK", "Slovak", ["Slovak"], "Europe"),
    "HU": CountryInfo("Hungary", "HU", "Hungarian", ["Hungarian"], "Europe"),
    "SI": CountryInfo("Slovenia", "SI", "Slovenian", ["Slovenian"], "Europe"),
    "HR": CountryInfo("Croatia", "HR", "Croatian", ["Croatian"], "Europe"),
    "BA": CountryInfo("Bosnia And Herzegovina", "BA", "Bosnian", ["Bosnian", "Croatian", "Serbian"], "Europe"),
    "RS": CountryInfo("Serbia", "RS", "Serbian", ["Serbian"], "Europe"),
    "ME": CountryInfo("Montenegro", "ME", "Montenegrin", ["Montenegrin", "Serbian"], "Europe"),
    "MK": CountryInfo("Macedonia", "MK", "Macedonian", ["Macedonian"], "Europe"),
    "AL": CountryInfo("Albania", "AL", "Albanian", ["Albanian"], "Europe"),
    "GR": CountryInfo("Greece", "GR", "Greek", ["Greek"], "Europe"),
    "BG": CountryInfo("Bulgaria", "BG", "Bulgarian", ["Bulgarian"], "Europe"),
    "RO": CountryInfo("Romania", "RO", "Romanian", ["Romanian"], "Europe"),
    "MD": CountryInfo("Moldova", "MD", "Romanian", ["Romanian", "Russian"], "Europe"),
    "UA": CountryInfo("Ukraine", "UA", "Ukrainian", ["Ukrainian", "Russian"], "Europe"),
    "BY": CountryInfo("Belarus", "BY", "Belarusian", ["Belarusian", "Russian"], "Europe"),
    "LT": CountryInfo("Lithuania", "LT", "Lithuanian", ["Lithuanian"], "Europe"),
    "LV": CountryInfo("Latvia", "LV", "Latvian", ["Latvian"], "Europe"),
    "EE": CountryInfo("Estonia", "EE", "Estonian", ["Estonian", "Russian"], "Europe"),
    "RU": CountryInfo("Russian Federation", "RU", "Russian", ["Russian"], "Europe"),
    "TR": CountryInfo("Turkey", "TR", "Turkish", ["Turkish"], "Europe"),
    "CY": CountryInfo("Cyprus", "CY", "Greek", ["Greek", "Turkish"], "Europe"),
    "MT": CountryInfo("Malta", "MT", "Maltese", ["Maltese", "English"], "Europe"),
    
    # Asia Pacific
    "JP": CountryInfo("Japan", "JP", "Japanese", ["Japanese"], "Asia Pacific"),
    "KR": CountryInfo("Korea", "KR", "Korean", ["Korean"], "Asia Pacific"),
    "KP": CountryInfo("North Korea", "KP", "Korean", ["Korean"], "Asia Pacific"),
    "CN": CountryInfo("China", "CN", "Chinese", ["Chinese"], "Asia Pacific"),
    "TW": CountryInfo("Taiwan", "TW", "Chinese", ["Chinese"], "Asia Pacific"),
    "HK": CountryInfo("Hong Kong", "HK", "Chinese", ["Chinese", "English"], "Asia Pacific"),
    "MO": CountryInfo("Macao", "MO", "Chinese", ["Chinese", "Portuguese"], "Asia Pacific"),
    "MN": CountryInfo("Mongolia", "MN", "Mongolian", ["Mongolian"], "Asia Pacific"),
    "KZ": CountryInfo("Kazakhstan", "KZ", "Kazakh", ["Kazakh", "Russian"], "Asia Pacific"),
    "UZ": CountryInfo("Uzbekistan", "UZ", "Uzbek", ["Uzbek", "Russian"], "Asia Pacific"),
    "KG": CountryInfo("Kyrgyzstan", "KG", "Kyrgyz", ["Kyrgyz", "Russian"], "Asia Pacific"),
    "TJ": CountryInfo("Tajikistan", "TJ", "Tajik", ["Tajik", "Russian"], "Asia Pacific"),
    "TM": CountryInfo("Turkmenistan", "TM", "Turkmen", ["Turkmen", "Russian"], "Asia Pacific"),
    "AF": CountryInfo("Afghanistan", "AF", "Dari", ["Dari", "Pashto"], "Asia Pacific"),
    "PK": CountryInfo("Pakistan", "PK", "Urdu", ["Urdu", "English"], "Asia Pacific"),
    "IN": CountryInfo("India", "IN", "Hindi", ["Hindi", "English"], "Asia Pacific"),
    "BD": CountryInfo("Bangladesh", "BD", "Bengali", ["Bengali", "English"], "Asia Pacific"),
    "BT": CountryInfo("Bhutan", "BT", "Dzongkha", ["Dzongkha", "English"], "Asia Pacific"),
    "NP": CountryInfo("Nepal", "NP", "Nepali", ["Nepali", "English"], "Asia Pacific"),
    "LK": CountryInfo("Sri Lanka", "LK", "Sinhala", ["Sinhala", "Tamil", "English"], "Asia Pacific"),
    "MV": CountryInfo("Maldives", "MV", "Dhivehi", ["Dhivehi", "English"], "Asia Pacific"),
    "MM": CountryInfo("Myanmar", "MM", "Burmese", ["Burmese", "English"], "Asia Pacific"),
    "TH": CountryInfo("Thailand", "TH", "Thai", ["Thai"], "Asia Pacific"),
    "LA": CountryInfo("Lao People's Democratic Republic", "LA", "Lao", ["Lao"], "Asia Pacific"),
    "KH": CountryInfo("Cambodia", "KH", "Khmer", ["Khmer", "English"], "Asia Pacific"),
    "VN": CountryInfo("Vietnam", "VN", "Vietnamese", ["Vietnamese"], "Asia Pacific"),
    "MY": CountryInfo("Malaysia", "MY", "Malay", ["Malay", "English", "Chinese"], "Asia Pacific"),
    "SG": CountryInfo("Singapore", "SG", "English", ["English", "Chinese", "Malay", "Tamil"], "Asia Pacific"),
    "BN": CountryInfo("Brunei Darussalam", "BN", "Malay", ["Malay", "English", "Chinese"], "Asia Pacific"),
    "ID": CountryInfo("Indonesia", "ID", "Indonesian", ["Indonesian"], "Asia Pacific"),
    "TL": CountryInfo("Timor-Leste", "TL", "Tetum", ["Tetum", "Portuguese"], "Asia Pacific"),
    "PH": CountryInfo("Philippines", "PH", "Filipino", ["Filipino", "English"], "Asia Pacific"),
    "AU": CountryInfo("Australia", "AU", "English", ["English"], "Asia Pacific"),
    "NZ": CountryInfo("New Zealand", "NZ", "English", ["English", "Maori"], "Asia Pacific"),
    "PG": CountryInfo("Papua New Guinea", "PG", "English", ["English", "Tok Pisin"], "Asia Pacific"),
    "FJ": CountryInfo("Fiji", "FJ", "English", ["English", "Fijian"], "Asia Pacific"),
    "VU": CountryInfo("Vanuatu", "VU", "Bislama", ["Bislama", "English", "French"], "Asia Pacific"),
    "NC": CountryInfo("New Caledonia", "NC", "French", ["French"], "Asia Pacific"),
    "SB": CountryInfo("Solomon Islands", "SB", "English", ["English"], "Asia Pacific"),
    "TO": CountryInfo("Tonga", "TO", "Tongan", ["Tongan", "English"], "Asia Pacific"),
    "WS": CountryInfo("Samoa", "WS", "Samoan", ["Samoan", "English"], "Asia Pacific"),
    "KI": CountryInfo("Kiribati", "KI", "English", ["English", "Gilbertese"], "Asia Pacific"),
    "TV": CountryInfo("Tuvalu", "TV", "Tuvaluan", ["Tuvaluan", "English"], "Asia Pacific"),
    "NR": CountryInfo("Nauru", "NR", "Nauruan", ["Nauruan", "English"], "Asia Pacific"),
    "PW": CountryInfo("Palau", "PW", "Palauan", ["Palauan", "English"], "Asia Pacific"),
    "FM": CountryInfo("Micronesia, Federated States Of", "FM", "English", ["English"], "Asia Pacific"),
    "MH": CountryInfo("Marshall Islands", "MH", "Marshallese", ["Marshallese", "English"], "Asia Pacific"),
    
    # Latin America
    "BR": CountryInfo("Brazil", "BR", "Portuguese", ["Portuguese"], "Latin America"),
    "AR": CountryInfo("Argentina", "AR", "Spanish", ["Spanish"], "Latin America"),
    "CL": CountryInfo("Chile", "CL", "Spanish", ["Spanish"], "Latin America"),
    "UY": CountryInfo("Uruguay", "UY", "Spanish", ["Spanish"], "Latin America"),
    "PY": CountryInfo("Paraguay", "PY", "Spanish", ["Spanish", "Guarani"], "Latin America"),
    "BO": CountryInfo("Bolivia", "BO", "Spanish", ["Spanish", "Quechua", "Aymara"], "Latin America"),
    "PE": CountryInfo("Peru", "PE", "Spanish", ["Spanish", "Quechua"], "Latin America"),
    "EC": CountryInfo("Ecuador", "EC", "Spanish", ["Spanish", "Quechua"], "Latin America"),
    "CO": CountryInfo("Colombia", "CO", "Spanish", ["Spanish"], "Latin America"),
    "VE": CountryInfo("Venezuela", "VE", "Spanish", ["Spanish"], "Latin America"),
    "GY": CountryInfo("Guyana", "GY", "English", ["English"], "Latin America"),
    "SR": CountryInfo("Suriname", "SR", "Dutch", ["Dutch", "English"], "Latin America"),
    "GF": CountryInfo("French Guiana", "GF", "French", ["French"], "Latin America"),
    
    # Middle East & Africa
    "TR": CountryInfo("Turkey", "TR", "Turkish", ["Turkish"], "Middle East"),
    "GE": CountryInfo("Georgia", "GE", "Georgian", ["Georgian"], "Middle East"),
    "AM": CountryInfo("Armenia", "AM", "Armenian", ["Armenian"], "Middle East"),
    "AZ": CountryInfo("Azerbaijan", "AZ", "Azerbaijani", ["Azerbaijani"], "Middle East"),
    "IR": CountryInfo("Iran, Islamic Republic Of", "IR", "Persian", ["Persian"], "Middle East"),
    "IQ": CountryInfo("Iraq", "IQ", "Arabic", ["Arabic", "Kurdish"], "Middle East"),
    "SY": CountryInfo("Syrian Arab Republic", "SY", "Arabic", ["Arabic"], "Middle East"),
    "LB": CountryInfo("Lebanon", "LB", "Arabic", ["Arabic", "French"], "Middle East"),
    "IL": CountryInfo("Israel", "IL", "Hebrew", ["Hebrew", "Arabic"], "Middle East"),
    "PS": CountryInfo("Palestinian Territory, Occupied", "PS", "Arabic", ["Arabic"], "Middle East"),
    "JO": CountryInfo("Jordan", "JO", "Arabic", ["Arabic"], "Middle East"),
    "SA": CountryInfo("Saudi Arabia", "SA", "Arabic", ["Arabic"], "Middle East"),
    "KW": CountryInfo("Kuwait", "KW", "Arabic", ["Arabic"], "Middle East"),
    "BH": CountryInfo("Bahrain", "BH", "Arabic", ["Arabic"], "Middle East"),
    "QA": CountryInfo("Qatar", "QA", "Arabic", ["Arabic"], "Middle East"),
    "AE": CountryInfo("United Arab Emirates", "AE", "Arabic", ["Arabic", "English"], "Middle East"),
    "OM": CountryInfo("Oman", "OM", "Arabic", ["Arabic"], "Middle East"),
    "YE": CountryInfo("Yemen", "YE", "Arabic", ["Arabic"], "Middle East"),
    
    # Africa
    "EG": CountryInfo("Egypt", "EG", "Arabic", ["Arabic"], "Africa"),
    "LY": CountryInfo("Libyan Arab Jamahiriya", "LY", "Arabic", ["Arabic"], "Africa"),
    "TN": CountryInfo("Tunisia", "TN", "Arabic", ["Arabic", "French"], "Africa"),
    "DZ": CountryInfo("Algeria", "DZ", "Arabic", ["Arabic", "French"], "Africa"),
    "MA": CountryInfo("Morocco", "MA", "Arabic", ["Arabic", "French"], "Africa"),
    "EH": CountryInfo("Western Sahara", "EH", "Arabic", ["Arabic"], "Africa"),
    "MR": CountryInfo("Mauritania", "MR", "Arabic", ["Arabic", "French"], "Africa"),
    "ML": CountryInfo("Mali", "ML", "French", ["French", "Bambara"], "Africa"),
    "NE": CountryInfo("Niger", "NE", "French", ["French"], "Africa"),
    "TD": CountryInfo("Chad", "TD", "French", ["French", "Arabic"], "Africa"),
    "SD": CountryInfo("Sudan", "SD", "Arabic", ["Arabic", "English"], "Africa"),
    "SS": CountryInfo("South Sudan", "SS", "English", ["English", "Arabic"], "Africa"),
    "ET": CountryInfo("Ethiopia", "ET", "Amharic", ["Amharic", "English"], "Africa"),
    "ER": CountryInfo("Eritrea", "ER", "Tigrinya", ["Tigrinya", "Arabic"], "Africa"),
    "DJ": CountryInfo("Djibouti", "DJ", "French", ["French", "Arabic"], "Africa"),
    "SO": CountryInfo("Somalia", "SO", "Somali", ["Somali", "Arabic"], "Africa"),
    "KE": CountryInfo("Kenya", "KE", "English", ["English", "Swahili"], "Africa"),
    "UG": CountryInfo("Uganda", "UG", "English", ["English", "Swahili"], "Africa"),
    "TZ": CountryInfo("Tanzania", "TZ", "Swahili", ["Swahili", "English"], "Africa"),
    "RW": CountryInfo("Rwanda", "RW", "Kinyarwanda", ["Kinyarwanda", "French", "English"], "Africa"),
    "BI": CountryInfo("Burundi", "BI", "Kirundi", ["Kirundi", "French"], "Africa"),
    "CD": CountryInfo("Congo, Democratic Republic", "CD", "French", ["French", "Lingala"], "Africa"),
    "CG": CountryInfo("Congo", "CG", "French", ["French"], "Africa"),
    "CF": CountryInfo("Central African Republic", "CF", "French", ["French", "Sango"], "Africa"),
    "CM": CountryInfo("Cameroon", "CM", "French", ["French", "English"], "Africa"),
    "GQ": CountryInfo("Equatorial Guinea", "GQ", "Spanish", ["Spanish", "French"], "Africa"),
    "GA": CountryInfo("Gabon", "GA", "French", ["French"], "Africa"),
    "ST": CountryInfo("Sao Tome And Principe", "ST", "Portuguese", ["Portuguese"], "Africa"),
    "AO": CountryInfo("Angola", "AO", "Portuguese", ["Portuguese"], "Africa"),
    "ZM": CountryInfo("Zambia", "ZM", "English", ["English"], "Africa"),
    "ZW": CountryInfo("Zimbabwe", "ZW", "English", ["English", "Shona"], "Africa"),
    "BW": CountryInfo("Botswana", "BW", "English", ["English", "Setswana"], "Africa"),
    "NA": CountryInfo("Namibia", "NA", "English", ["English", "Afrikaans"], "Africa"),
    "ZA": CountryInfo("South Africa", "ZA", "English", ["English", "Afrikaans", "Zulu"], "Africa"),
    "LS": CountryInfo("Lesotho", "LS", "Sesotho", ["Sesotho", "English"], "Africa"),
    "SZ": CountryInfo("Swaziland", "SZ", "Swati", ["Swati", "English"], "Africa"),
    "MG": CountryInfo("Madagascar", "MG", "Malagasy", ["Malagasy", "French"], "Africa"),
    "MU": CountryInfo("Mauritius", "MU", "English", ["English", "French", "Creole"], "Africa"),
    "SC": CountryInfo("Seychelles", "SC", "English", ["English", "French", "Creole"], "Africa"),
    "KM": CountryInfo("Comoros", "KM", "Comorian", ["Comorian", "French", "Arabic"], "Africa"),
    "YT": CountryInfo("Mayotte", "YT", "French", ["French"], "Africa"),
    "RE": CountryInfo("Reunion", "RE", "French", ["French"], "Africa"),
    "MZ": CountryInfo("Mozambique", "MZ", "Portuguese", ["Portuguese"], "Africa"),
    "MW": CountryInfo("Malawi", "MW", "English", ["English", "Chichewa"], "Africa"),
    "GH": CountryInfo("Ghana", "GH", "English", ["English"], "Africa"),
    "TG": CountryInfo("Togo", "TG", "French", ["French"], "Africa"),
    "BJ": CountryInfo("Benin", "BJ", "French", ["French"], "Africa"),
    "BF": CountryInfo("Burkina Faso", "BF", "French", ["French"], "Africa"),
    "CI": CountryInfo("Cote D'Ivoire", "CI", "French", ["French"], "Africa"),
    "LR": CountryInfo("Liberia", "LR", "English", ["English"], "Africa"),
    "SL": CountryInfo("Sierra Leone", "SL", "English", ["English"], "Africa"),
    "GN": CountryInfo("Guinea", "GN", "French", ["French"], "Africa"),
    "GW": CountryInfo("Guinea-Bissau", "GW", "Portuguese", ["Portuguese", "French"], "Africa"),
    "GM": CountryInfo("Gambia", "GM", "English", ["English"], "Africa"),
    "SN": CountryInfo("Senegal", "SN", "French", ["French"], "Africa"),
    "GM": CountryInfo("Gambia", "GM", "English", ["English"], "Africa"),
    "CV": CountryInfo("Cape Verde", "CV", "Portuguese", ["Portuguese"], "Africa"),
}

# Legacy region mapping for backward compatibility
LEGACY_REGION_MAP = {
    "California": "US",
    "Texas": "US", 
    "Nevada": "US",
    "New York": "US",
    "Florida": "US",
    "Costa Rica": "CR",
    "Mexico": "MX",
    "Canada": "CA",
    "UK": "GB",
    "Germany": "DE",
    "France": "FR",
    "Japan": "JP",
    "Australia": "AU",
    "Brazil": "BR",
    "Italy": "IT",
    "Spain": "ES",
    "China": "CN",
    "India": "IN",
    "South Korea": "KR",
    "Russia": "RU"
}

def get_country_by_code(country_code: str) -> Optional[CountryInfo]:
    """Get country information by ISO country code"""
    return COUNTRY_LANGUAGE_MAP.get(country_code.upper())

def get_country_by_name(country_name: str) -> Optional[CountryInfo]:
    """Get country information by country name"""
    for country in COUNTRY_LANGUAGE_MAP.values():
        if country.name.lower() == country_name.lower():
            return country
    return None

def get_legacy_region_mapping(region: str) -> Optional[str]:
    """Convert legacy region names to country codes"""
    return LEGACY_REGION_MAP.get(region)

def get_primary_language(country_code: str) -> str:
    """Get the primary language for a country"""
    country = get_country_by_code(country_code)
    return country.primary_language if country else "English"

def get_supported_languages(country_code: str) -> List[str]:
    """Get all supported languages for a country"""
    country = get_country_by_code(country_code)
    return country.languages if country else ["English"]

def get_countries_by_region(region: str) -> List[CountryInfo]:
    """Get all countries in a specific region"""
    return [country for country in COUNTRY_LANGUAGE_MAP.values() if country.region == region]

def get_all_countries() -> List[CountryInfo]:
    """Get all available countries"""
    return list(COUNTRY_LANGUAGE_MAP.values())

def search_countries(query: str) -> List[CountryInfo]:
    """Search countries by name or code"""
    query = query.lower()
    results = []
    
    for country in COUNTRY_LANGUAGE_MAP.values():
        if (query in country.name.lower() or 
            query in country.code.lower() or
            query in country.primary_language.lower()):
            results.append(country)
    
    return results

def get_country_selector_data() -> Dict:
    """Get data formatted for frontend country selector"""
    return {
        "countries": [
            {
                "code": country.code,
                "name": country.name,
                "primary_language": country.primary_language,
                "languages": country.languages,
                "region": country.region
            }
            for country in sorted(COUNTRY_LANGUAGE_MAP.values(), key=lambda x: x.name)
        ],
        "regions": list(set(country.region for country in COUNTRY_LANGUAGE_MAP.values()))
    }
