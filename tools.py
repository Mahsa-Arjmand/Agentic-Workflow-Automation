from langchain.tools import tool
from database import (
    get_all_functionalities,
    get_functionality_by_code,
    get_categories,
    increment_usage,
    log_usage,
)

KEYWORD_MAPPINGS = {
    "general": ["appointment", "schedule", "doctor", "visit", "GP"],
    "heart": ["cardiologist", "cardiology", "specialist", "referral"],
    "bone": ["orthopedist", "orthopedic", "specialist", "referral"],
    "brain": ["neurologist", "neurology", "specialist", "referral"],
    "kidney": ["nephrologist", "nephrology", "specialist"],
    "skin": ["dermatologist", "dermatology", "specialist"],
    "eye": ["ophthalmologist", "ophthalmology", "specialist"],
    "child": ["pediatric", "pediatrician", "specialist"],
    "woman": ["gynecologist", "gynecology", "specialist"],
    "pregnant": ["obstetrician", "obstetrics", "specialist"],
    "mental": ["psychiatrist", "psychiatry", "specialist"],
    "cancer": ["oncologist", "oncology", "specialist"],
    "surgery": ["operation", "surgical", "admission", "inpatient"],
    "xray": ["x-ray", "radiology", "test results", "lab"],
    "x-ray": ["radiology", "test results", "lab"],
    "mri": ["radiology", "test results", "lab"],
    "ct": ["CT scan", "radiology", "test results"],
    "blood": ["lab", "test results", "blood work"],
    "prescription": ["refill", "medication", "pharmacy", "drug"],
    "medicine": ["refill", "pharmacy", "medication", "drug"],
    "medication": ["refill", "pharmacy", "drug"],
    "pill": ["refill", "pharmacy", "OTC", "medication"],
    "receipt": ["bill", "payment", "billing", "invoice"],
    "invoice": ["bill", "payment", "billing"],
    "expensive": ["payment plan", "installment", "billing"],
    "cheap": ["insurance", "coverage", "payment plan"],
    "appointment": ["schedule", "book", "visit", "doctor"],
    "cancel": ["cancel appointment", "reschedule"],
    "change": ["reschedule", "change plan", "switch"],
    "ambulance": ["emergency", "dispatch", "transport", "115"],
    "accident": ["emergency", "ER", "ambulance", "urgent"],
    "dying": ["emergency", "ambulance", "ER", "urgent"],
    "urgent": ["emergency", "walk-in", "ER", "ambulance"],
    "today": ["walk-in", "same day", "urgent", "appointment"],
    "now": ["emergency", "walk-in", "urgent"],
    "room": ["admission", "inpatient", "private room", "stay"],
    "discharge": ["leave hospital", "check out", "going home"],
    "food": ["room service", "meal", "diet"],
    "specialist": ["referral", "cardiologist", "neurologist", "consultation"],
    "second opinion": ["referral", "consultation", "another doctor"],
    "note": ["doctor note", "sick note", "certificate", "work"],
    "history": ["medical history", "records", "previous", "conditions"],
    "allergy": ["medical history", "allergies", "records"],
    "insurance": ["coverage", "claim", "Tamin", "Salamat", "verify"],
    "claim": ["insurance claim", "reimbursement", "submit", "money"],
    "refund": ["reimbursement", "claim", "money back"],
    "pay": ["bill", "payment", "billing", "invoice"],
    "cost": ["bill", "payment", "price", "how much"],
    "price": ["bill", "payment", "cost", "how much"],
    "owe": ["bill", "payment", "balance", "outstanding"],
    "balance": ["bill", "payment", "outstanding", "how much"],
    "result": ["test results", "lab", "report", "blood work"],
    "report": ["test results", "lab", "medical records"],
    "lost": ["reprint", "copy", "prescription", "replace"],
    "forgot": ["reprint", "copy", "prescription", "replace"],
    "copy": ["reprint", "prescription", "medical records"],
    "visit": ["appointment", "schedule", "book", "doctor"],
    "see doctor": ["appointment", "schedule", "visit", "book"],
    "need doctor": ["appointment", "schedule", "visit", "book"],
    "sick": ["appointment", "doctor note", "walk-in", "urgent"],
    "pain": ["appointment", "walk-in", "emergency", "urgent"],
    "hurt": ["appointment", "walk-in", "emergency", "urgent"],
    "referral": ["specialist", "consultation", "cardiologist", "neurologist"],
    "refer": ["specialist", "referral", "consultation"],
}


@tool
def search_functionalities(query: str) -> str:
    """
    Search for matching hospital services based on patient query.
    Use FIRST when patient describes a problem.
    Input: Patient's question or problem description.
    Handles synonyms and related terms automatically.
    """
    functionalities = get_all_functionalities()
    query_lower = query.lower()
    results = []

    expanded_terms = list(query_lower.split())
    
    for key, values in KEYWORD_MAPPINGS.items():
        if key in query_lower:
            expanded_terms.extend(values)
    
    expanded_terms = list(set(expanded_terms))

    for func in functionalities:
        search_text = f"{func['title']} {func['description']} {func['keywords']} {func['category_name']}".lower()
        
        original_matches = sum(1 for kw in query_lower.split() if kw in search_text)
        expanded_matches = sum(1 for kw in expanded_terms if kw in search_text)
        
        total_matches = max(original_matches, expanded_matches)
        
        if total_matches > 0:
            results.append({
                'code': func['code'],
                'title': func['title'],
                'description': func['description'],
                'category_icon': func['category_icon'],
                'category_name': func['category_name'],
                'keywords': func['keywords'],
                'access_path': func['access_path'],
                'usage_count': func['usage_count'],
                'matches': total_matches,
            })

    results.sort(key=lambda x: x['matches'], reverse=True)

    if not results:
        return "No matching hospital services found."

    output = " Matching Hospital Services:\n\n"
    for i, r in enumerate(results[:5], 1):
        output += f"{i}. {r['category_icon']} **{r['code']} - {r['title']}** ({r['matches']} matches)\n"
        output += f"   {r['description'][:100]}...\n\n"
    
    return output


@tool
def get_steps(functionality_code: str) -> str:
    """
    Get detailed step-by-step guide for a specific hospital service.
    Use AFTER finding a matching functionality code.
    Input: Functionality code like 'APT-001', 'MED-001', 'BIL-001'.
    """
    func = get_functionality_by_code(functionality_code.upper().strip())
    
    if not func:
        return f"Code '{functionality_code}' not found."

    increment_usage(func['code'])
    log_usage(func['code'], f"Steps retrieved for {functionality_code}")

    output = f"## {func['category_icon']} {func['code']} — {func['title']}\n\n"
    output += f"**Category:** {func['category_name']}\n"
    output += f"**Description:** {func['description']}\n"
    output += f"**Keywords:** {func['keywords']}\n"
    output += f"**Access:** `{func['access_path']}`\n\n"
    output += "**Steps:**\n"
    for step in func['steps'].split('\n'):
        output += f"- {step.strip()}\n"
    
    return output


@tool
def list_categories(query: str = "") -> str:
    """
    Show all available hospital service categories.
    Use when patient wants to browse options or see all services.
    """
    categories = get_categories()
    all_funcs = get_all_functionalities()

    output = " **Hospital Service Categories:**\n\n"

    for cat in categories:
        funcs = [f for f in all_funcs if f['category_id'] == cat['id']]
        output += f"### {cat['icon']} {cat['name']}\n"
        output += f"> {cat['description']}\n\n"
        for f in funcs:
            output += f"- **{f['code']}** — {f['title']}\n"
        output += "\n"

    output += " Use any code with `get_steps` for detailed instructions."
    return output


@tool
def search_by_keyword(keyword: str) -> str:
    """
    Quick search by single keyword.
    Use when patient mentions a specific word like 'appointment', 'test', 'bill', 'emergency'.
    Also checks keyword mappings for related terms.
    """
    all_funcs = get_all_functionalities()
    keyword_lower = keyword.lower().strip()
    
    search_terms = [keyword_lower]
    if keyword_lower in KEYWORD_MAPPINGS:
        search_terms.extend(KEYWORD_MAPPINGS[keyword_lower])
    
    matches = []
    seen_codes = set()
    
    for term in search_terms:
        for func in all_funcs:
            if func['code'] in seen_codes:
                continue
            search_text = f"{func['title']} {func['keywords']} {func['description']} {func['category_name']}".lower()
            if term in search_text:
                matches.append(func)
                seen_codes.add(func['code'])

    if not matches:
        return f"No hospital service found for keyword: '{keyword}'"

    output = f" Hospital services matching '{keyword}':\n\n"
    for func in matches[:5]:
        output += f"- **{func['code']}** — {func['title']} ({func['category_icon']} {func['category_name']})\n"

    return output


ALL_TOOLS = [
    search_functionalities,
    get_steps,
    list_categories,
    search_by_keyword,
]