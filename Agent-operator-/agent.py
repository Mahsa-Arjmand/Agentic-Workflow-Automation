import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config import LM_STUDIO_API_BASE, LM_STUDIO_API_KEY, LM_STUDIO_MODEL
from tools import ALL_TOOLS


def create_agent():
    
    llm = ChatOpenAI(
        base_url=LM_STUDIO_API_BASE,
        api_key=LM_STUDIO_API_KEY,
        model=LM_STUDIO_MODEL,
        temperature=0.7,
        max_tokens=800,
        timeout=60,
    )

    class HospitalAgent:
        def __init__(self, llm, tools):
            self.llm = llm
            self.tools = {t.name: t for t in tools}

        def invoke(self, input_dict):
            query = input_dict.get("input", "")
            query_lower = query.lower()

            category_phrases = [
                "show all", "list all", "browse", "what do you have",
                "all services", "all categories", "what services",
                "what's available", "what is available",
            ]
            if any(w in query_lower for w in category_phrases):
                return self._handle_categories()

            words = [w for w in query_lower.split() if len(w) > 2]
            if len(words) <= 2:
                result = self._handle_keyword_search(query)
                output_text = str(result.get("output", ""))
                if "No hospital service found" in output_text:
                    return self._handle_functionality(query)
                return result

            return self._handle_functionality(query)

        def _handle_categories(self):
           
            result = self.tools["list_categories"].invoke("")
            cat_text = str(result)

            prompt = f"""The hospital database returned these categories:
{cat_text}

Present them in a friendly way in English. Use emojis, make it easy to read.
Talk like a helpful hospital receptionist."""

            try:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                answer = response.content if hasattr(response, 'content') else str(response)
            except:
                answer = cat_text

            return {"output": answer + "\n\n---\n **Tool:** `list_categories` →  Database"}

        def _handle_keyword_search(self, query):
            """Quick keyword search."""
            result = self.tools["search_by_keyword"].invoke(query)
            search_text = str(result)
            
            codes = re.findall(r'\b([A-Z]{3}-\d{3})\b', search_text)
            if codes:
                return self._show_solution(codes[0], query)

            return {"output": search_text}

        def _handle_functionality(self, query):
            result = self.tools["search_functionalities"].invoke(query)
            search_text = str(result)
            
            codes = re.findall(r'\b([A-Z]{3}-\d{3})\b', search_text)
            if codes:
                return self._show_solution(codes[0], query)

            prompt = f"""A patient said: "{query}"

No exact match was found in the hospital system.

Respond like a friendly hospital receptionist:
- Apologize briefly
- Suggest what they might be looking for
- Ask them to describe their issue in a different way
- Mention examples: appointment, test results, billing, medication, emergency
- Keep it warm and helpful"""

            try:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                answer = response.content if hasattr(response, 'content') else str(response)
            except:
                answer = "I couldn't find a matching service. Could you describe your issue differently? For example, is it about an appointment, test results, billing, or medication?"

            return {"output": answer + "\n\n---\n **Tool:** `search_functionalities` → No match found"}

        def _show_solution(self, code, query):
            """Show solution for a matched functionality."""
            from database import get_functionality_by_code
            func = get_functionality_by_code(code)
            
            if not func:
                return {"output": f"Found code {code} but couldn't get details."}

            self.tools["get_steps"].invoke(code)

            prompt = f"""You are a friendly hospital receptionist. A patient asked: "{query}"

The hospital system has this solution:
{func['steps']}

Respond in a casual, friendly way in ENGLISH. 
Talk like a helpful hospital staff member.
Use emojis. Be warm and caring.
Make the patient feel comfortable and well taken care of.
Give them the COMPLETE solution - don't hold back any steps.
Don't ask questions - just give them the solution clearly."""

            try:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                answer = response.content if hasattr(response, 'content') else str(response)
            except:
                answer = f"Here's how we can help with {func['title']}:\n\n{func['steps']}"

            output = answer
            output += f"""
            
---
### Behind the Scenes:

| Step | Tool | Result |
|------|------|--------|
| 1. Search | `search_functionalities` | Found: **{code}** |
| 2. Get Steps | `get_steps("{code}")` |  Retrieved |

**Selected:** `{code}` — {func['title']} ({func['category_icon']} {func['category_name']})
"""
            return {"output": output}

    return HospitalAgent(llm, ALL_TOOLS)