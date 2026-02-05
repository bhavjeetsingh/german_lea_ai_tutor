from typing import List, Optional
from openai import OpenAI
from google import genai
from google.genai import types
from groq import Groq
from src.config.settings import settings
from src.models.schemas import Message, StudentProfile


class AIService:
    """Service for AI integration with OpenAI, Google Gemini, or Groq."""
    
    def __init__(self):
        self.provider = settings.ai_provider
        
        # Debug: Print loaded configuration
        print(f"[AI Service] Initializing with provider: {self.provider}")
        
        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key is not set. Please check your .env file.")
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
            print(f"[AI Service] OpenAI initialized with model: {self.model}")
            
        elif self.provider == "gemini":
            if not settings.gemini_api_key:
                raise ValueError("Gemini API key is not set. Please check your .env file.")
            self.client = genai.Client(api_key=settings.gemini_api_key)
            self.model = settings.gemini_model
            print(f"[AI Service] Gemini initialized with model: {self.model}")
            
        elif self.provider == "groq":
            if not settings.groq_api_key:
                raise ValueError("Groq API key is not set. Please check your .env file.")
            self.client = Groq(api_key=settings.groq_api_key)
            self.model = settings.groq_model
            print(f"[AI Service] Groq initialized with model: {self.model}")
        else:
            raise ValueError(f"Unknown AI provider: {self.provider}")
    
    def _build_system_prompt(self, profile: StudentProfile, teaching_mode: Optional[str] = None) -> str:
        """Build system prompt based on student profile and teaching mode."""
        
        base_prompt = f"""You are Lea, a calm, structured, and human-like German language tutor from GermanLeap.

Student Profile:
- Name: {profile.name}
- Current Level: {profile.current_level}
- Goals: {', '.join(profile.goals) if profile.goals else 'General German learning'}
- Target Exam: {profile.target_exam or 'None'}
- Career Interest: {profile.career_interest or 'Not specified'}

Your Teaching Style:
- Calm, patient, and encouraging
- Structured and organized in explanations
- Realistic and honest about German learning challenges
- Provide examples in both German and English
- Adjust difficulty based on student's level ({profile.current_level})
- Focus on practical, real-world German usage

"""
        
        mode_prompts = {
            "grammar_practice": "Focus on teaching German grammar with clear explanations, examples, and exercises appropriate for their level.",
            "vocabulary_building": "Help build vocabulary through context-based learning, themed word groups, and practical usage examples.",
            "speaking_practice": "Engage in realistic German conversations appropriate for their level, correcting mistakes gently and providing alternatives.",
            "exam_preparation": "Provide Goethe/Telc exam-style questions and practice, focusing on test strategies and common patterns.",
            "interview_coaching": "Coach for German job interviews with realistic scenarios, common questions, and professional language.",
            "career_guidance": "Provide safe, realistic advice about career paths in Germany (Ausbildung, nursing, skilled jobs), qualifications needed, and next steps."
        }
        
        if teaching_mode and teaching_mode in mode_prompts:
            base_prompt += f"\nCurrent Teaching Mode: {teaching_mode.replace('_', ' ').title()}\n{mode_prompts[teaching_mode]}"
        
        return base_prompt
    
    async def get_response(
        self,
        profile: StudentProfile,
        messages: List[Message],
        teaching_mode: Optional[str] = None
    ) -> str:
        """Get AI response from the configured provider."""
        
        system_prompt = self._build_system_prompt(profile, teaching_mode)
        
        if self.provider == "openai":
            return await self._get_openai_response(system_prompt, messages)
        elif self.provider == "gemini":
            return await self._get_gemini_response(system_prompt, messages)
        elif self.provider == "groq":
            return await self._get_groq_response(system_prompt, messages)
    
    async def _get_openai_response(self, system_prompt: str, messages: List[Message]) -> str:
        """Get response from OpenAI."""
        
        formatted_messages = [{"role": "system", "content": system_prompt}]
        
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[AI Service] OpenAI Error: {str(e)}")
            raise
    
    async def _get_gemini_response(self, system_prompt: str, messages: List[Message]) -> str:
        """Get response from Google Gemini."""
        
        # Build conversation history with system prompt
        conversation_parts = [system_prompt + "\n\n"]
        
        for msg in messages:
            if msg.role == "user":
                conversation_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                conversation_parts.append(f"Assistant: {msg.content}")
        
        # Add the final prompt
        full_prompt = "\n\n".join(conversation_parts)
        
        try:
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            return response.text
        except Exception as e:
            print(f"[AI Service] Gemini Error: {str(e)}")
            raise
    
    async def _get_groq_response(self, system_prompt: str, messages: List[Message]) -> str:
        """Get response from Groq."""
        
        formatted_messages = [{"role": "system", "content": system_prompt}]
        
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[AI Service] Groq Error: {str(e)}")
            raise


ai_service = AIService()