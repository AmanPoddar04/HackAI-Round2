import os
import dotenv

dotenv.load_dotenv()

print(os.environ.get("PALM_API_KEY"))
