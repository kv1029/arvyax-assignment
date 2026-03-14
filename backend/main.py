# -------------------- IMPORTS --------------------
from fastapi import FastAPI  # Imports the core API framework
from pydantic import BaseModel  # Helps validate the incoming JSON data structure
from motor.motor_asyncio import AsyncIOMotorClient  # Connects to MongoDB asynchronously
import os  # Lets us read the operating system's environment variables
from dotenv import load_dotenv  # Loads the secret .env file
import google.generativeai as genai  # NEW: Imports the Google Gemini SDK
import json  # NEW: Helps us parse the text response from Gemini into a real JSON object
from collections import Counter  # NEW: Helps us quickly count the most common emotions and ambiences


# -------------------- INITIAL SETUP --------------------
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))  # This executes immediately to load our secret passwords
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL")  # Grabs your database connection string securely
print(MONGO_URL)
print("Mongo URL:", MONGO_URL)
client = AsyncIOMotorClient(MONGO_URL)  # Connects to your MongoDB cluster
db = client.journal_db  # Creates or selects the database
collection = db.entries  # Creates or selects the collection to store entries

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


# -------------------- DATA MODELS --------------------
class JournalEntry(BaseModel):
    userId: str
    ambience: str
    text: str
    emotion: str = None  # NEW: Optional field to save the AI result
    keywords: list = []  # NEW: Optional field to save the AI keywords
    summary: str = None  # NEW: Optional field to save the AI summary


class AnalyzeRequest(BaseModel):
    text: str


# -------------------- ROUTE 1: CREATE ENTRY --------------------
@app.post("/api/journal")
async def create_entry(entry: JournalEntry):

    entry_dict = entry.model_dump()

    result = await collection.insert_one(entry_dict)

    return {
        "message": "Entry saved",
        "id": str(result.inserted_id)
    }


# -------------------- ROUTE 2: GET ENTRIES BY USER --------------------
@app.get("/api/journal/{userId}")  # Listens for GET requests and captures the userId
async def get_entries(userId: str):

    # Finds all documents matching this specific user
    cursor = collection.find({"userId": userId})

    # Loads up to 100 matching entries into a list
    entries = await cursor.to_list(length=100)

    # Converts MongoDB ObjectId to string so it can be sent as JSON
    for entry in entries:
        entry["_id"] = str(entry["_id"])

    # Returns all matching entries
    return entries


# -------------------- ROUTE 3: LLM EMOTION ANALYSIS --------------------
@app.post("/api/journal/analyze")
async def analyze_journal(request: AnalyzeRequest):

    # This strict prompt forces Gemini to only return the exact JSON the assignment demands
    prompt = f"""
    Analyze this journal entry: "{request.text}"
    Return ONLY a valid JSON object with no markdown formatting. It must have exactly these keys:
    "emotion": a single word describing the main feeling.
    "keywords": an array of 3 important words from the text.
    "summary": a 1-sentence summary of the experience.
    """

    response = model.generate_content(prompt)

    # Clean Gemini response if it returns ```json formatting
    cleaned_text = response.text.replace("```json", "").replace("```", "").strip()

    # Convert text to JSON
    result_json = json.loads(cleaned_text)

    return result_json


# -------------------- ROUTE 4: GET USER INSIGHTS --------------------
@app.get("/api/journal/insights/{userId}")
async def get_insights(userId: str):

    # Fetch all entries for this user
    cursor = collection.find({"userId": userId})

    entries = await cursor.to_list(length=100)

    total_entries = len(entries)

    if total_entries == 0:
        return {
            "totalEntries": 0,
            "topEmotion": "none",
            "mostUsedAmbience": "none",
            "recentKeywords": []
        }

    # Extract ambiences and emotions
    ambiences = [entry.get("ambience") for entry in entries if entry.get("ambience")]
    emotions = [entry.get("emotion") for entry in entries if entry.get("emotion")]

    # Collect all keywords
    all_keywords = []
    for entry in entries:
        all_keywords.extend(entry.get("keywords", []))

    # Calculate most common ambience and emotion
    most_used_ambience = Counter(ambiences).most_common(1)[0][0] if ambiences else "unknown"
    top_emotion = Counter(emotions).most_common(1)[0][0] if emotions else "unknown"

    # Get top 3 keywords
    recent_keywords = [k[0] for k in Counter(all_keywords).most_common(3)]

    return {
        "totalEntries": total_entries,
        "topEmotion": top_emotion,
        "mostUsedAmbience": most_used_ambience,
        "recentKeywords": recent_keywords
    }  