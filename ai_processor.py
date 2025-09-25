import os
import json
import re
from typing import List, Dict, Any
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class AIProcessor:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.openai_key:
            self.client = OpenAI(api_key=self.openai_key)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove basic emojis and special characters
        text = re.sub(r'[^\w\s\-\.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_issues_llm(self, product_id: str, texts: List[str]) -> List[Dict[str, Any]]:
        """Extract issues using LLM"""
        if not self.client:
            return self.extract_issues_rule_based(product_id, texts)
        
        try:
            batch_text = "\n".join([f"- {text}" for text in texts[:50]])
            
            prompt = f"""Analyze the following product feedback texts and extract recurring fit or care issues. 
Return ONLY a JSON array where each item has these exact fields:
- product_id: "{product_id}"  
- issue_category: "fit" or "care"
- body_area: specific area like "waist", "sleeve", "length", "color", etc (or "" if general)
- descriptor: short snake_case like "runs_small", "color_fade", "shrink", etc
- severity: integer 1-5 (1=minor, 5=severe)
- frequency_hint: integer 0-100 (rough percentage of texts mentioning this issue)

Focus on recurring problems, ignore compliments. Merge similar phrases.

Texts:
{batch_text}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            # Try to extract JSON from response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                issues = json.loads(json_str)
                return [issue for issue in issues if isinstance(issue, dict)]
            else:
                logger.warning(f"No JSON found in LLM response for {product_id}")
                return self.extract_issues_rule_based(product_id, texts)
                
        except Exception as e:
            logger.error(f"LLM extraction failed for {product_id}: {e}")
            return self.extract_issues_rule_based(product_id, texts)
    
    def extract_issues_rule_based(self, product_id: str, texts: List[str]) -> List[Dict[str, Any]]:
        """Fallback rule-based extraction"""
        issues = []
        
        # Define keyword mappings
        size_keywords = {
            "runs_small": ["tight", "small", "snug", "narrow"],
            "runs_large": ["loose", "baggy", "large", "big", "oversized"],
            "sleeve_short": ["sleeve short", "short sleeve", "sleeves short"],
            "sleeve_long": ["sleeve long", "long sleeve", "sleeves long"],
            "length_short": ["short length", "too short", "length short"],
            "length_long": ["long length", "too long", "length long"]
        }
        
        care_keywords = {
            "color_fade": ["color faded", "color fade", "fading", "color bleed"],
            "shrink": ["shrink", "shrunk", "shrinkage"],
            "stretch": ["stretch", "stretched", "stretchy"],
            "wrinkle": ["wrinkle", "wrinkled", "creased"]
        }
        
        body_areas = {
            "waist": ["waist", "torso", "middle"],
            "sleeve": ["sleeve", "arm", "shoulder"],
            "length": ["length", "hem", "long", "short"],
            "color": ["color", "fade", "bleed"],
            "overall": ["overall", "general", "fit"]
        }
        
        combined_text = " ".join([self.clean_text(text) for text in texts]).lower()
        
        # Check fit issues
        for descriptor, keywords in size_keywords.items():
            matches = sum(1 for kw in keywords if kw in combined_text)
            if matches > 0:
                severity = 3  # Base severity
                if "very" in combined_text or "extremely" in combined_text:
                    severity += 1
                elif "slightly" in combined_text:
                    severity -= 1
                
                # Determine body area
                body_area = ""
                for area, area_keywords in body_areas.items():
                    if any(akw in combined_text for akw in area_keywords):
                        body_area = area
                        break
                
                frequency = min(100, (matches / len(texts)) * 100)
                
                issues.append({
                    "product_id": product_id,
                    "issue_category": "fit",
                    "body_area": body_area,
                    "descriptor": descriptor,
                    "severity": max(1, min(5, severity)),
                    "frequency_hint": int(frequency)
                })
        
        # Check care issues
        for descriptor, keywords in care_keywords.items():
            matches = sum(1 for kw in keywords if kw in combined_text)
            if matches > 0:
                severity = 3
                if "very" in combined_text or "extremely" in combined_text:
                    severity += 1
                
                body_area = "color" if "color" in descriptor else ""
                frequency = min(100, (matches / len(texts)) * 100)
                
                issues.append({
                    "product_id": product_id,
                    "issue_category": "care",
                    "body_area": body_area,
                    "descriptor": descriptor,
                    "severity": max(1, min(5, severity)),
                    "frequency_hint": int(frequency)
                })
        
        return issues
    
    def generate_copy(self, product_id: str, issues: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate size guidance and care tips"""
        if not issues:
            return {"size_guidance": "", "care_tip": ""}
        
        if self.client:
            return self.generate_copy_llm(product_id, issues)
        else:
            return self.generate_copy_rule_based(issues)
    
    def generate_copy_llm(self, product_id: str, issues: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate copy using LLM"""
        try:
            issues_text = json.dumps(issues, indent=2)
            
            prompt = f"""Given these structured fit and care issues for product {product_id}:
{issues_text}

Generate concise, helpful copy. Return ONLY JSON with exactly these fields:
- size_guidance: clear sizing advice (≤300 characters, customer-friendly, neutral tone)  
- care_tip: actionable care instructions (≤200 characters, practical, materials-agnostic)

Be specific and helpful. Don't repeat the product ID."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                return {
                    "size_guidance": result.get("size_guidance", "")[:300],
                    "care_tip": result.get("care_tip", "")[:200]
                }
            else:
                return self.generate_copy_rule_based(issues)
                
        except Exception as e:
            logger.error(f"LLM copy generation failed for {product_id}: {e}")
            return self.generate_copy_rule_based(issues)
    
    def generate_copy_rule_based(self, issues: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate copy using templates"""
        fit_issues = [i for i in issues if i.get("issue_category") == "fit"]
        care_issues = [i for i in issues if i.get("issue_category") == "care"]
        
        # Generate size guidance
        size_guidance = ""
        if fit_issues:
            top_fit = max(fit_issues, key=lambda x: x.get("severity", 0) * x.get("frequency_hint", 0))
            descriptor = top_fit.get("descriptor", "")
            
            if descriptor == "runs_small":
                size_guidance = "Consider ordering one size up for a more comfortable fit."
            elif descriptor == "runs_large":
                size_guidance = "Consider ordering one size down for a better fit."
            elif "sleeve_short" in descriptor:
                size_guidance = "Note that sleeves may run shorter than expected."
            elif "length_short" in descriptor:
                size_guidance = "This item may run shorter in length than expected."
            else:
                size_guidance = "Check size chart carefully before ordering."
        
        # Generate care tip
        care_tip = ""
        if care_issues:
            top_care = max(care_issues, key=lambda x: x.get("severity", 0) * x.get("frequency_hint", 0))
            descriptor = top_care.get("descriptor", "")
            
            if "color_fade" in descriptor:
                care_tip = "Wash inside out in cold water to preserve color."
            elif "shrink" in descriptor:
                care_tip = "Air dry or use low heat to prevent shrinkage."
            elif "stretch" in descriptor:
                care_tip = "Lay flat to dry to maintain shape."
            else:
                care_tip = "Follow care label instructions for best results."
        
        return {
            "size_guidance": size_guidance[:300],
            "care_tip": care_tip[:200]
        }