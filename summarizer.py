"""AI-powered meeting summarization module using local Ollama models."""
import os
from dotenv import load_dotenv

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Load environment variables
load_dotenv()


class Summarizer:
    """Summarizer for generating meeting summaries using local Ollama models."""

    def __init__(self, model_name=None, base_url=None):
        """
        Initialize the summarizer.

        Args:
            model_name: Ollama model name (default: from env or 'llama3.2')
            base_url: Ollama server URL (default: http://localhost:11434)
        """
        if not OLLAMA_AVAILABLE:
            raise ImportError(
                "Ollama package not installed. Please run: pip install ollama"
            )

        self.model_name = model_name or os.getenv('OLLAMA_MODEL', 'llama3.2')
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

        # Configure ollama client if base_url is provided
        if self.base_url != 'http://localhost:11434':
            self.client = ollama.Client(host=self.base_url)
        else:
            self.client = ollama

        print(f"Using Ollama model: {self.model_name}")
        self._check_model_availability()

    def _check_model_availability(self):
        """Check if the specified model is available locally."""
        try:
            # List available models
            models = self.client.list()
            available_models = [model['name'] for model in models.get('models', [])]

            # Check if our model is available (match on base name)
            model_base = self.model_name.split(':')[0]
            model_available = any(model_base in m for m in available_models)

            if not model_available:
                print(f"\n⚠️  Warning: Model '{self.model_name}' not found locally.")
                print(f"   Available models: {', '.join(available_models) if available_models else 'None'}")
                print(f"\n   To download the model, run:")
                print(f"   ollama pull {self.model_name}")
                print(f"\n   Recommended models:")
                print(f"   - llama3.2 (small, fast)")
                print(f"   - llama3.2:3b (good balance)")
                print(f"   - llama3.1:8b (better quality)")
                print(f"   - mistral (alternative)")
                print(f"   - qwen2.5:7b (multilingual)")

        except Exception as e:
            print(f"\n⚠️  Could not check model availability: {e}")
            print(f"   Make sure Ollama is running: ollama serve")

    def generate_summary(self, transcript, meeting_title=None, custom_prompt=None):
        """
        Generate a summary of the meeting transcript.

        Args:
            transcript: The meeting transcript text
            meeting_title: Optional meeting title for context
            custom_prompt: Optional custom prompt for summarization

        Returns:
            Dictionary containing summary and key points
        """
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = self._build_default_prompt(transcript, meeting_title)

        print("Generating meeting summary with local Ollama model...")
        print(f"Using model: {self.model_name}")

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'num_predict': 2000,  # Max tokens to generate
                }
            )

            summary = response['response']
            print("Summary generated successfully!")

            return {
                'summary': summary,
                'model': self.model_name
            }

        except Exception as e:
            print(f"Error generating summary: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure Ollama is running: ollama serve")
            print(f"2. Make sure the model is downloaded: ollama pull {self.model_name}")
            print("3. Check if Ollama is accessible at:", self.base_url)
            raise

    def _build_default_prompt(self, transcript, meeting_title):
        """Build the default prompt for summarization."""
        title_context = f"Meeting Title: {meeting_title}\n\n" if meeting_title else ""

        prompt = f"""{title_context}Please analyze the following meeting transcript and provide a comprehensive summary with the following sections:

1. **Executive Summary**: A brief 2-3 sentence overview of the meeting
2. **Key Discussion Points**: Main topics discussed (bullet points)
3. **Decisions Made**: Any decisions or conclusions reached
4. **Action Items**: Tasks assigned with responsible parties if mentioned
5. **Next Steps**: Follow-up actions or future meeting plans

Transcript:
{transcript}

Please format your response clearly with headers for each section."""

        return prompt

    def save_summary(self, summary_data, output_path):
        """
        Save the summary to a file.

        Args:
            summary_data: Dictionary containing summary information
            output_path: Path to save the summary

        Returns:
            Path to the saved summary file
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=== MEETING SUMMARY ===\n\n")
            f.write(summary_data['summary'])
            f.write(f"\n\n---\nGenerated by: {summary_data['model']}\n")

        print(f"Summary saved to: {output_path}")
        return output_path

    def summarize_and_save(self, transcript, output_dir='summaries',
                          meeting_title=None, filename=None):
        """
        Convenience method to summarize and save in one step.

        Args:
            transcript: The meeting transcript text
            output_dir: Directory to save summaries
            meeting_title: Optional meeting title
            filename: Optional custom filename

        Returns:
            Tuple of (summary_path, summary_text)
        """
        # Generate summary
        summary_data = self.generate_summary(transcript, meeting_title)

        # Generate filename if not provided
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.txt"

        output_path = os.path.join(output_dir, filename)

        # Save
        self.save_summary(summary_data, output_path)

        return output_path, summary_data['summary']
