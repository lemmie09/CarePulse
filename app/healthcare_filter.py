HEALTHCARE_TERMS = [
    "doctor", "doctors", "physician", "clinic", "medical", "medicine",
    "hospital", "healthcare", "health care", "primary care", "family medicine",
    "internal medicine", "urgent care", "walk-in clinic", "medical center",
    "dentist", "dental", "orthodont", "orthodontics", "oral surgeon", "dds", "dmd",
    "optometrist", "ophthalmologist", "eye care", "vision",
    "pediatric", "pediatrics", "children's clinic",
    "psychiatrist", "psychologist", "mental health", "counseling", "therapy", "therapist",
    "obgyn", "gynecology", "obstetrics", "women's health",
    "dermatology", "dermatologist",
    "orthopedic", "sports medicine", "spine", "joint", "pain management",
    "chiropractic", "chiropractor",
    "rehab", "rehabilitation", "physical therapy",
    "surgeon", "specialist", "nurse", "nursing", "hospice"
]

NON_HEALTHCARE_EXCLUSIONS = [
    "restaurant", "restaurants", "bar", "bbq", "barbacoa", "tacos", "burger",
    "pizza", "food", "eatery", "cafe", "coffee", "bakery", "grill", "market",
    "brewery", "pub", "salon", "hair", "nails", "spa", "massage",
    "fitness", "gym", "yoga", "hotel", "travel", "auto", "car wash",
    "pet", "dog", "cat", "home cleaning", "shopping"
]

def is_healthcare_category(categories):
    text = str(categories).lower()

    has_healthcare = any(term in text for term in HEALTHCARE_TERMS)
    has_non_healthcare = any(term in text for term in NON_HEALTHCARE_EXCLUSIONS)

    return has_healthcare and not has_non_healthcare
