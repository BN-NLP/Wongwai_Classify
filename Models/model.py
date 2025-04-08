from typing import Literal, List, Optional
from pydantic import BaseModel
from enum import Enum

class SentimentItem(BaseModel):
    """ Represents sentiment anlysis of social comment.
    - explanation: explained in detailed why you choose this sentiment.
    - output:the sentiment value of phase for TRUE company. if it's sarcasm, considerate it as negative.
    **MUST ANSWER EVERY PHASE!!**
    """
    explanation: str
    output: Literal["Positive", "Negative", "Neutral"]

class TRUEDTACItem(BaseModel):
    """Represents if phase related to TRUE or DTAC company or not.
    - explanation: explained in detailed why this phase related to TRUE or DTAC company.
    - output is this phase related to TRUE or DTAC company, only if it mention in phase that it's about TRUE or DTAC.
    NOTE: synonym of TRUE is 'ค่ายแดง','ค่ายตัว t'.
          synonym of DTAC is 'Dtac', 'DTAC', 'ดีแทค', 'ค่ายฟ้า', 'detac', 'dtac', '1678'
    NOTE: "Nan" means not related to TRUE or DTAC.
    **MUST ANSWER EVERY PHASE!!**
    """
    explanation: str
    output: Literal["True", "Dtac", "Nan"]

# class ADS(BaseModel):
#     """Represents commercial ads and commercial phase detection.
#     - explanation: explained in detailed why you this this phase is commercial.
#     - output is this phase is ads.
#     **MUST ANSWER EVERY PHASE!!**
#     """
#     explanation: str
#     ADS: Literal[True, False]

class SentimentTrue(BaseModel):
    Sentiment: list[SentimentItem]
    IS_TRUE: list[TRUEDTACItem]
    # ADS: list[ADS]

class ClassifyItem(BaseModel):
    """Represents classification of TRUE or DTAC company.
    - explanation: explained in detailed why you choose classify for this phases.
    **MUST ANSWER EVERY PHASE!!**
    """
    explanation: str

class OutputOptions(str, Enum):
    True_5G = "True 5G"
    True_Visions = "True Visions"
    True_Visions_NOW = "True Visions NOW"
    True_Online = "True Online"
    True_You = "True You"
    True_ID = "True ID"
    True_iService = "True iService"
    True_Corp = "True Corp"
    True_ = "True"
    Dtac = "Dtac"
    Nan = "Nan"

class Item(BaseModel):
    """จะตอบคำถาม user ต้องแสดงข้อมูลอะไรบ้างจากข้อมูลข้างล่าง
    คำอธิบาย:

    "True 5G" - ชื่อเดิม True 5G = True Move H, dtac 5G = dtac
    อินเตอร์เน็ตมือถือ, ให้บริการเชื่อมต่อเครือข่ายที่แข็งแกร่งและรวดเร็วครอบคลุมทั่วไทย
    ในฐานะผู้นำบริการโทรคมนาคมเพียงรายเดียวที่มีคลื่นความถี่ครบทุก 8 ย่าน ทั้งเครือข่าย 5G และ 4G
    ด้วยจำนวนเสาสัญญาณที่มีมากกว่าหลายหมื่นแห่งทั่วประเทศ พร้อมให้บริการเครือข่ายครอบคลุม 99% ของประชากรแล้ว

    "True Visions" - True Visions = บริการ Premium Cable TV แบบ Subscription ให้บริการคอนเทนต์ช่องดังระดับโลก
    ที่สามารถรับชมความบันเทิง ทั้งหนัง ซีรีส์ กีฬา วาไรตี้ สารคดี การ์ตูน และข่าว ทั้งไทยและต่างประเทศ

    "True Visions NOW" - True Visions NOW = แพ็กเกจสตรีมมิ่ง กีฬาสดมากที่สุดในไทย และช่องบันเทิงสุดฮิต

    "True Online" - เน็ตบ้าน, อินเตอร์เน็ตไฟเบอร์ครบวงจร, Convergence Service, Smart Home, IoT,
    บริการติดตั้งระบบอินเตอร์เน็ตไฟเบอร์ความเร็วสูง, Business Solution, Home Fiber Internet ขาย Bundle
    บริการร่วมกับ True Visions และ True 5G

    "True You" - สิทธิประโยชน์, สิทธิพิเศษสำหรับลูกค้าทรู โดยแบ่ง Tier ตามแบรนด์ ดังนี้
      True = True You
      Tier = Black Card, Red Card, Blue Card, Green Card, White Card
      Currency = True Point / Point

    "True ID" - แอปพลิเคชัน เว็บไซต์ และกล่องทรูไอดี ทีวี ที่เต็มไปด้วยความบันเทิง (Extra - Tainment)
    และเข้าถึงทุกบริการจากทรูในรูปแบบต่างๆไม่ว่าจะเป็นการชำระเงิน การจัดเก็บข้อมูล
    การให้บริการคอนเทนต์ทั้งไทยและต่างประเทศ รวมถึงสิทธิประโยชน์ต่างๆ จากทรูอีกมากมาย

    "True iService" - แอปพลิเคชัน เว็บไซต์ ช่องทางอำนวยความสะดวกสำหรับลูกค้า ในการเข้าถึงบริการและผลิตภัณฑ์ต่างๆ ในกลุ่มทรู
    ไม่ว่าจะเป็นการตรวจสอบยอดการใช้งาน ประวัติใบแจ้งค่าบริการ ชำระค่าบริการ เติมเงิน สมัครแพ็กเกจ เสริม ตรวจสอบข้อมูลส่วนตัวได้ด้วยตัวคุณเองในรูปแบบออนไลน์
    ทรู ไอเซอร์วิส, ดีแทค แอปฯ

    "True Corp" - เดิม: บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน) (TRUE) และ บริษัท โทเทิ่ล แอ็คเซ็ส คอมมูนิเคชั่น จำกัด (มหาชน) (DTAC)
    เป็นพลังขับเคลื่อนเชื่อมโยงผู้คน กลุ่มธุรกิจ และสังคม ให้เติบโตก้าวหน้าอย่างยั่งยืน ทั้งจากบริการโทรผ่านเสียงและการใช้งานดาต้าระดับเวิลด์คลาสของทรู
    ระบบนิเวศดิจิทัลที่ตอบโจทย์ทุกไลฟ์สไตล์ของชีวิต ตลอดจนความบันเทิงระดับโลก การมอบสิทธิพิเศษ และการให้บริการเชื่อมต่อแบบไร้รอยต่อ ยิ่งไปกว่านั้น
    ทรู คอร์ปอเรชั่น ยังมุ่งนำเทคโนโลยีปัญญาประดิษฐ์ (AI) สร้างสรรค์นวัตกรรม ร่วมสร้างคุณค่าให้โลกมีความสมบูรณ์ยั่งยืนและปลอดภัยยิ่งกว่า

    "True" - หมายถึงการพูดถึงทรูในลักษณะกว้าง ๆ โดยไม่ได้ระบุผลิตภัณฑ์หรือบริการเฉพาะเจาะจง
    เช่น การกล่าวถึงบริษัททรู, แบรนด์ทรู, หรือบริการทรูโดยรวม หากในข้อความมีการพูดถึงคำว่า
    'ทรู' หรือ 'True' โดยไม่มีคำอื่นที่เกี่ยวข้องกับผลิตภัณฑ์หรือบริการเฉพาะ
    - **!!หากไม่สามารถ จำแนก product ทรูได้ชัดเจน ให้ตอบ "TRUE"**

    "dtac" - ชื่อเดิม dtac 5G = dtac
    อินเตอร์เน็ตมือถือ, ให้บริการเชื่อมต่อเครือข่ายที่แข็งแกร่งและรวดเร็วครอบคลุมทั่วไทย
    ในฐานะผู้นำบริการโทรคมนาคมเพียงรายเดียวที่มีคลื่นความถี่ครบทุก 8 ย่าน ทั้งเครือข่าย 5G และ 4G
    ด้วยจำนวนเสาสัญญาณที่มีมากกว่าหลายหมื่นแห่งทั่วประเทศ พร้อมให้บริการเครือข่ายครอบคลุม 99% ของประชากรแล้ว

    "์Nan" - ในข้อความไม่ได้เกี่ยวอะไรกับ product TRUE หรือ DTAC หรือ ผลิตภัณฑ์ หรือ ไม่มีการพูดถึง ทรู หรือ ดีแทค เช่น สนใจค่ะ
    """
    output: OutputOptions

class ClassifyTrue(BaseModel):
    Classify: ClassifyItem
    Classify_output: Item


system_prompt = """

PERSONA:
You're Social Analysis from TRUE or DTAC Company, a telecom company with multiple partners.

TASKS:
1. Classify the product of from user quotes return one-by-one.

INPUT SOURCE
Many phases gathered from news tablets and Facebook pages.


**Classify Section**
You are an AI model that classifies user quotes into one or more True Corporation services.
Follow these classification rules with high accuracy and efficiency:

🔹 **Level 1: ตรวจสอบว่ามี "ทรู" หรือ "true" หรือ "ค่ายแดง" หรือ "1242" หรือ "Dtac" หรือ "ดีแทค" หรือ "1678" ในข้อความหรือไม่**
   - **ถ้ามี** → ดำเนินการจำแนกตามหมวดหมู่ด้านล่าง
   - **ถ้าไม่มี** → ให้ classify เป็น `"Nan"` ทันที

🔹 **Level 2: ตรวจสอบประเภทผลิตภัณฑ์ (ถ้ามี "ทรู" หรือ "true" หรือ "ค่ายแดง" หรือ "1242")**
1. **True You**: หากพบ **"ร้านเด็ด"**, **"คะแนน"**, **"แต้ม"**, **"จัดแคมเปญ"**, **"truepoint"**.
2. **True Corp**: หากพบ **"คอร์ปอเรชั่น"**, **"บริษัท ทรู"**, **"ซีอีโอทรู"**, **"ทรูดีแทค"**, **"ทรู ดิจิทัล กรุ๊ป"**, **"จับมือ"**,
   **"ทรู ต้อนรับ"**, **"เอส เอฟ จับมือ ทรูดีแทค"**, **"บริษัทฯ"**, **"ลูกค้าทรู ดีแทค"**, **"True + Dtac"**.
3. **True iService**: หากพบ **"true iservice"**, **"ทรู เซอร์วิส"**, **"แจ้งยอดชำระ"**, **"True Service"**, **"ไอเซอร์วิส"**.
4. **True Visions NOW**: หากพบ **"TrueVisions Now"**, **"TrueVisions Now Max"**, **"รวมความบันเทิงจากช่องชั้นนำของทรูวิชั่นส์"**, **"TVS NOWS"**.
5. **True Visions**: หากพบ **"ทรูวิชั่น"**, **"truevision"**, **"ทรูส์วิชั่น"**, **"TRUE Vision"**.
6. **True ID**: หากพบ **"True id"**, **"ทรูไอดี"**, **"TrueID"**, **"trueid"**.
7. **True Online**: หากพบ **"เน็ตบ้าน"**, **"true fiber"**, **"ทรูไฟเบอร์"**, **"ติดตั้งเน็ตบ้าน"**, **"Fiber Stand alone"**, **"โปรย้ายค่ายเน็ตบ้าน"**,
   **"WiFiที่บ้าน"**, **"Fiber"**, **"แพ็กเกจเน็ตบ้านไฟเบอร์True"**, **"กล่องเราท์เตอร์แดง"**, **"แพคเกจเน็ตบ้านทรู"**, **"สนใจติดตั้งเน็ทบ้าน"**, **"True wifi"**.
8. **True 5G**: หากพบ **"เน็ตโทรศัพท์"**, **"เปิดเน็ตเบอร์โทร"**, **"อินเตอร์เน็ตแบบเติมเงิน"**, **"ทรูมูฟ"**, **"ซิม"**, **"โปรโมชั่น"**, **"Truedtac5G"**
   **"เครือข่ายดีแทค"**, **"เปิดสัญญาณ"**, **"มือถือเก่ามาเเลกใหม่"**, **"แพคเกจ"**, **"ย้ายค่าย"**, **"เน็ททรู"**, **"eSIM"**,
   **"เบอร์รายเดือน"**, **"เน็ตดีแทค"**, **"trueshop"**, **"ทรูช็อป"**, **"เล่นเน็ตไม่อั้น"**, **"คลื่น"**, **"โปรข้ามเวลา"**, **"รายเดือนTruemove"**,
   **"รายเดือนทรู"**, **"เน็ตทรูกับดีแทค"**, **"โทรมาขายโปร"**, **"ทรูแบบเติมเงิน"**, **"ทรูช่วยยกเลิกเน็ต"**, **"เก็บค่าบริการโรมมิ่ง"**,
   **"เน็ตทรูรายเดือนคุ้มๆ"**, **"สมัครโรมมิ่งทรู"**, **"เบอร์ทรู"**.
9. **TRUE (General Category)**: หากพบ **"ค่ายแดง"**, **"สัญญาณ"**, **"true"**, **"ย้ายค่าย"**, **"ทรู"**, **"ช่องทรู"**, **"กล่องทรู"**,
   **"พนักงานทรู"**, **"เน็ต"**, **"เจ้าหน้าที่ทรู"**, **"ติดต่อทรู"**, **"1242"**, **"เปิดสัญญาณทรู"**, **"กลยุทธ์ของทรู"**, **"สาขาทรู"**
   ➜ **รวมถึงกรณีที่พูดถึง "เน็ต" แต่ไม่ได้ระบุว่าเป็น "เน็ตบ้าน" หรือ "เน็ตโทรศัพท์"**
   ➜ **ให้ classify เป็น `"TRUE"`**

   **Level 3: ตรวจสอบประเภทผลิตภัณฑ์ (ถ้ามี "Dtac" หรือ "ดีแทค" หรือ "1678")**
   **Dtac**: หากพบ "Dtac, DTAC, ดีแทค, ค่ายฟ้า, detac, dtac, 1678"

"""

system_prompt_2 = """
PERSONA:
You're Social Analysis from TRUE Company, a telecom company with multiple partners.

TO DO: !!MUST ANSWER EVERY PHASE **CANNOT SKIP OR RETURN NONE FOR ANY PHASE**
ALWAYS RETURN OUTPUT FOR EVERY PHASE, EVEN IF IT'S UNKNOWN.

TASKS:
1. Find the sentiment of these user quotes and return the output format for all {phase} phases one-by-one.

INPUT SOURCE:
Many phases about TRUE gathered from news tablets and TRUE Facebook pages.

BASIC CRITERIA FOR SENTIMENT ANALYSIS:
- If it's just a commercial ad or commercial phase (e.g., phases with # are likely to be ads), classify it as Neutral.
- If the phase benefits, compliments, or shows interest in TRUE Company or TRUE Products, classify it as Positive.
- Conversely, if the phase is bad for TRUE Company's reputation, classify it as Negative.
- If the phase shows interest such as "สนใจ", classify it as Positive.

!!IMPORTANT: RETURN OUTPUT FOR EVERY INPUT PHASE. DO NOT OMIT ANY ITEM!!
"""