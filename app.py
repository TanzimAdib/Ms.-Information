from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def check_claim(claim):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {"role": "system", "content": """You are a strict fact-checker. Classify the claim into exactly one category: True, False, Neutral, Rumor, Myth, Religious Claim, Conspiracy Theory, or Gibberish.

Respond in EXACTLY this format, nothing else:
VERDICT: [category] 
CONFIDENCE: [High/Medium/Low] 
REASON: [five sentence explaining why this claim belongs in that category] 
"""},
            {"role": "user", "content": claim}   
        ])

    return response.choices[0].message.content

st.title("Ms. Information - Fact Checker")
st.write("Claim or statement to be fact checked ")

st.write("Try examples: ")
examples = ["Earth is flat", "Sky is blue", "blaaHahah", "Moon landing was faked", "Vaccines contain tracking device"]
cols = st.columns(len(examples))
def claim_ver(claim):
    if claim:
        with st.spinner("Checking your claim ..."):
            result = check_claim(claim)
        
        lines = result.strip().split("\n")
        verdict_line = ""
        confidence_line = ""
        reason_line = ""
        
        for l in lines:
            if l.startswith("VERDICT"):
                verdict_line = l
            elif l.startswith("CONFIDENCE"):
                confidence_line = l
            elif l.startswith("REASON"):
                reason_line = l
        
        st.markdown(f"{verdict_line}")
        st.markdown(f"{confidence_line}")
        st.markdown(reason_line)
    else:
        st.warning("Try Again")

for i, ex in enumerate(cols):
    if ex.button(examples[i]):
        claim_ver(examples[i])


claim = st.text_input("Claim")

if st.button("Check"):
    claim_ver(claim)
