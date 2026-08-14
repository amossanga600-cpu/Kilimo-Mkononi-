import os
from google import genai
from google.genai import types

# 1. Kuchukua API Key kutoka kwenye Mfumo/Server (Environment Variable)
# Hakikisha umeweka GEMINI_API_KEY kwenye .env au mazingira ya server yako.
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY haijapatikana! Tafadhali weka API key kwenye Environment Variables.")

# 2. Kutengeneza Client ya Google GenAI
client = genai.Client(api_key=api_key)

# 3. Maelekezo Maalum (System Instructions) ya Kuzuia AI Kujibu Mambo Yasiyohusu Kilimo
SYSTEM_INSTRUCTION = """
Wewe ni mtaalamu wa kilimo na mifugo unayeitwa Mshauri wa Kilimo Mkononi nchini Tanzania.

MAJUKUMU YAKO:
1. Kutoa ushauri wa kitaalamu na sahihi kuhusu kilimo, udongo, pembejeo, na matunzo ya mazao (mfano: kabichi, mahindi, mboga na matunda).
2. Kutambua magonjwa ya mazao na kutoa tiba/dawa sahihi zinazopatikana Afrika Mashariki/Tanzania.
3. Kutoa mwongozo wa maandalizi ya shamba na vipindi vya kupanda.

MASHARTI YA KUFUATA STRICTLY:
- Jibu maswali yote kwa Kiswahili rahisi na kinachoeleweka vyema na mkulima wa kawaida.
- Jiambatishe kama mtaalamu rasmi kutoka 'Kilimo Mkononi'.
- KAMA MTUMIAJI AKIKUULIZA SWALI LISILOHUSU KILIMO, MIFUGO, AU MAZINGIRA YA UZALISHAJI (mfano: mpira, siasa, muziki, au hesabu za shuleni):
  Mjibu kwa heshima hivi: "Samahani, mimi ni Mshauri wa Kilimo Mkononi. Naweza kukusaidia pekee kwenye masuala yanayohusu kilimo, mifugo, na afya ya mazao. Tafadhali niulize swali linalohusu kilimo."
"""

def uliza_mshauri_wa_kilimo(swali_la_mkulima: str) -> str:
    """
    Kazi hii inachukua swali la mkulima, inalituma Gemini AI,
    na kurudisha jibu lililochujwa la kilimo tu.
    """
    try:
        # Configuration za mfumo
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.6,  # Kutoa majibu thabiti na ya kweli
        )
        
        # Kutuma ombi kwenda Gemini API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=swali_la_mkulima,
            config=config,
        )
        
        return response.text

    except Exception as e:
        return f"Samahani, imetokea hitilafu ya kiufundi kwenye mfumo wa Kilimo Mkononi: {str(e)}"

# --- SEHEMU YA KUJARIBU KODI (TESTING) ---
if __name__ == "__main__":
    print("--- Jaribio la Mshauri wa Kilimo Mkononi ---")
    
    # Jaribio 1: Swali la Kilimo
    swali_1 = "Kabichi inahitaji mbolea gani wakati wa kupanda?"
    print(f"\nSwali: {swali_1}")
    print(f"Jibu:\n{uliza_mshauri_wa_kilimo(swali_1)}")
    
    # Jaribio 2: Swali lisilohusu Kilimo (Ili kupima ulinzi)
    swali_2 = "Man City vs Arsenal nani alishinda?"
    print(f"\nSwali: {swali_2}")
    print(f"Jibu:\n{uliza_mshauri_wa_kilimo(swali_2)}")
