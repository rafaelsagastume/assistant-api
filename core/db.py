import motor.motor_asyncio

from core.config import MONGODB_URL

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

db = client.get_database("assistant")

organizations = db.get_collection("organizations")
users = db.get_collection("users")
apikeys = db.get_collection("apikeys")
assitants = db.get_collection("assistants")
files = db.get_collection("assistants_files")
vectors = db.get_collection("assistants_vectors")
