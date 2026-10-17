"""
GramSetu AI - Agriculture Math & Seed/Fertilizer Calculators
Provides exact scientific measurements per acre/bigha.
"""
import re

def calculate_agri_requirements(prompt: str, user_land_str: str = None) -> dict:
    lower = prompt.lower()

    # Extract acres from prompt or fallback to user_land_str
    acre_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)', prompt, re.IGNORECASE)
    acres = None
    if acre_match:
        acres = float(acre_match.group(1))
    elif user_land_str:
        m_saved = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)', user_land_str, re.IGNORECASE)
        if m_saved:
            acres = float(m_saved.group(1))

    # Detect crop
    crop = "wheat"
    crop_name = "Wheat (गेहूं)"
    if re.search(r'\b(mustard|sarson)\b', lower):
        crop = "mustard"
        crop_name = "Mustard (सरसों)"
    elif re.search(r'\b(rice|dhan|paddy)\b', lower):
        crop = "rice"
        crop_name = "Paddy/Rice (धान)"

    if acres is None:
        acres = 1.0  # Default standard 1 acre calculation

    # Calculations
    res = {}
    if crop == "wheat":
        min_seed = round(acres * 40, 1)
        max_seed = round(acres * 45, 1)
        dap_bags = round(acres * 1, 1)
        urea_bags = round(acres * 2, 1)
        potash_bags = round(acres * 0.5, 1)
        zinc_kg = round(acres * 10, 1)

        res["tool_name"] = "Agri Calculator (Seed & Fertilizer)"
        res["badge"] = f"🌾 Calculated for {acres} Acre(s) of {crop_name}"
        res["text"] = (
            f"🌾 **{crop_name} Seed & Fertilizer Calculation for {acres} Acre(s):**\n\n"
            f"1. **Seed Requirement (बीज मात्रा):**\n"
            f"   • समय पर बुवाई: **{min_seed} से {max_seed} किलोग्राम** ({min_seed/100:.2f} से {max_seed/100:.2f} क्विंटल) बीज।\n"
            f"   • पछेती बुवाई (दिसंबर): **{round(acres*50, 1)} से {round(acres*55, 1)} किलोग्राम** बीज।\n\n"
            f"2. **Fertilizer Requirement (खाद की मात्रा):**\n"
            f"   • **DAP (50kg बैग):** **{dap_bags} बैग** (बुवाई के समय Basal).\n"
            f"   • **Urea (45kg बैग):** **{urea_bags} बैग** (21 दिन और 45 दिन की सिंचाई पर 2 बार में).\n"
            f"   • **MOP पोटाश (50kg बैग):** **{potash_bags} बैग**.\n"
            f"   • **जिंक सल्फेट (33%):** **{zinc_kg} kg**."
        )

    elif crop == "mustard":
        min_seed = round(acres * 1.5, 2)
        max_seed = round(acres * 2.0, 2)
        ssp_bags = round(acres * 1, 1)
        urea_bags = round(acres * 0.8, 1)
        sulphur_kg = round(acres * 10, 1)

        res["tool_name"] = "Agri Calculator (Mustard)"
        res["badge"] = f"🌼 Calculated for {acres} Acre(s) of {crop_name}"
        res["text"] = (
            f"🌼 **{crop_name} Seed & Fertilizer Calculation for {acres} Acre(s):**\n\n"
            f"1. **Seed Requirement (बीज मात्रा):** **{min_seed} से {max_seed} किलोग्राम**।\n"
            f"2. **Fertilizer Requirement:** **{ssp_bags} बैग SSP (50kg)** + **{urea_bags} बैग यूरिया** + **{sulphur_kg} kg सल्फर 90%**."
        )

    elif crop == "rice":
        hybrid_seed = round(acres * 6, 1)
        basmati_seed = round(acres * 10, 1)
        res["tool_name"] = "Agri Calculator (Rice)"
        res["badge"] = f"🌾 Calculated for {acres} Acre(s) of {crop_name}"
        res["text"] = (
            f"🌾 **{crop_name} Seed Requirement for {acres} Acre(s):**\n\n"
            f"• **Hybrid धान:** **{hybrid_seed} किलोग्राम**।\n"
            f"• **बासमती / देसी किस्में:** **{basmati_seed} किलोग्राम**।"
        )

    return res

def convert_land_area(acres: float, target_unit: str = None) -> dict:
    acres = max(0.0001, float(acres))
    pucca_bigha = round(acres * 1.6, 2)
    kaccha_bigha = round(acres * 4.8, 2)
    sq_yards_num = int(round(acres * 4840))
    sq_feet_num = int(round(acres * 43560))
    sq_yards = f"{sq_yards_num:,}"
    sq_feet = f"{sq_feet_num:,}"
    hectares = round(acres * 0.404686, 3)
    kanal = int(round(acres * 8))
    marla = int(round(acres * 160))
    kattha = round(acres * 26.6, 1)

    # Format acres nicely (e.g. 1 instead of 1.0)
    acres_str = f"{acres:g}"

    # Target unit specific lead line
    lead_highlight = ""
    if target_unit in ["feet", "foot", "sq_feet", "sqft"]:
        lead_highlight = f"📐 **{acres_str} Acre = {sq_feet} Square Feet (वर्ग फुट)**\n\n"
    elif target_unit in ["yard", "yards", "gaj"]:
        lead_highlight = f"📐 **{acres_str} Acre = {sq_yards} Square Yards / Gaj (वर्ग गज)**\n\n"
    elif target_unit in ["bigha", "pucca_bigha"]:
        lead_highlight = f"📐 **{acres_str} Acre = {pucca_bigha} Pucca Bigha (पक्का बीघा)**\n\n"
    elif target_unit in ["hectare", "ha"]:
        lead_highlight = f"📐 **{acres_str} Acre = {hectares} Hectare (हेक्टेयर)**\n\n"

    text = (
        f"{lead_highlight}"
        f"📐 **Land Area Calculation for {acres_str} Acre(s) (भूमि माप गणना):**\n\n"
        f"1. **Universal Measurement Units (सार्वभौमिक इकाइयां):**\n"
        f"   • **Square Feet (वर्ग फुट):** **{sq_feet} sq. ft** (1 Acre = 43,560 sq. ft)\n"
        f"   • **Square Yards (वर्ग गज / Gaj):** **{sq_yards} sq. yards** (1 Acre = 4,840 sq. yards)\n"
        f"   • **Hectares (हेक्टेयर):** **{hectares} Ha** (1 Hectare = 2.471 Acres)\n\n"
        f"2. **State & Regional Conversions (क्षेत्रीय बीघा व कनाल):**\n"
        f"   • **UP & Rajasthan (पक्का बीघा):** **{pucca_bigha} Bigha** (1 Bigha = 27,225 sq. ft = 3,025 sq. yards)\n"
        f"   • **Western UP & Haryana (कच्चा बीघा):** **{kaccha_bigha} Bigha**\n"
        f"   • **Punjab & Haryana:** **{kanal} Kanal** ({marla} Marla)\n"
        f"   • **Bihar & Jharkhand:** **{round(acres * 1.33, 2)} Bigha** ({kattha} Kattha)"
    )

    return {
        "acres": acres,
        "pucca_bigha": pucca_bigha,
        "kaccha_bigha": kaccha_bigha,
        "sq_yards": sq_yards,
        "sq_feet": sq_feet,
        "hectares": hectares,
        "kanal": kanal,
        "marla": marla,
        "text": text.strip()
    }

def convert_land_area_from_prompt(prompt: str) -> dict:
    """
    Parses natural language land measurement queries and performs exact conversions.
    Handles: '1 acre land in feet', '5 bigha in acre', '2 hectare to feet', etc.
    """
    lower = prompt.lower().strip()

    # Determine target unit if asked
    target_unit = None
    if re.search(r'\b(feet|foot|ft|sq\s*ft|sqft|square\s*feet|फुट|फिट)\b', lower):
        target_unit = "feet"
    elif re.search(r'\b(gaj|yard|yards|sq\s*yard|square\s*yard|गज)\b', lower):
        target_unit = "gaj"
    elif re.search(r'\b(bigha|bighas|बीघा)\b', lower) and not re.search(r'\b(\d+(?:\.\d+)?)\s*(?:bigha|bighas|बीघा)\b', lower):
        target_unit = "bigha"
    elif re.search(r'\b(hectare|hectares|हेक्टेयर|ha)\b', lower) and not re.search(r'\b(\d+(?:\.\d+)?)\s*(?:hectare|hectares|हेक्टेयर)\b', lower):
        target_unit = "hectare"

    # 1. Acre match
    m_acre = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)', lower)
    if m_acre:
        acres = float(m_acre.group(1))
        return convert_land_area(acres, target_unit=target_unit)

    # 2. Bigha match
    m_bigha = re.search(r'(\d+(?:\.\d+)?)\s*(?:bigha|bighas|बीघा)', lower)
    if m_bigha:
        bigha = float(m_bigha.group(1))
        acres = bigha / 1.6
        return convert_land_area(acres, target_unit=target_unit or "feet")

    # 3. Hectare match
    m_ha = re.search(r'(\d+(?:\.\d+)?)\s*(?:hectare|hectares|हेक्टेयर|ha)', lower)
    if m_ha:
        ha = float(m_ha.group(1))
        acres = ha * 2.47105
        return convert_land_area(acres, target_unit=target_unit or "feet")

    # 4. Sq feet match
    m_ft = re.search(r'(\d+(?:\.\d+)?)\s*(?:sq\s*ft|sqft|square\s*feet|feet|foot|फुट)', lower)
    if m_ft:
        feet = float(m_ft.group(1))
        acres = feet / 43560.0
        return convert_land_area(acres, target_unit="bigha")

    # 5. Gaj / Sq Yards match
    m_gaj = re.search(r'(\d+(?:\.\d+)?)\s*(?:gaj|sq\s*yard|square\s*yard|yard|yards|गज)', lower)
    if m_gaj:
        gaj = float(m_gaj.group(1))
        acres = gaj / 4840.0
        return convert_land_area(acres, target_unit=target_unit or "feet")

    # Default fallback: 1 Acre
    return convert_land_area(1.0, target_unit=target_unit or "feet")

