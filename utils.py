"""Utility functions for DroidRun UX Explorer"""
import os
from pathlib import Path


def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent


def load_prompt(prompt_name):
    """Load a prompt template from the prompts folder
    
    Args:
        prompt_name: Name of the prompt file (with or without .txt extension)
    
    Returns:
        str: Content of the prompt file
    """
    if not prompt_name.endswith('.txt'):
        prompt_name += '.txt'
    
    prompt_path = get_project_root() / 'prompts' / prompt_name
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    except Exception as e:
        raise Exception(f"Error loading prompt {prompt_name}: {str(e)}")


def format_prompt(template, **kwargs):
    """Format a prompt template with provided variables
    
    Args:
        template: Prompt template string
        **kwargs: Variables to format into the template
    
    Returns:
        str: Formatted prompt
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise KeyError(f"Missing required variable in prompt template: {e}")


def load_and_format_prompt(prompt_name, **kwargs):
    """Load and format a prompt in one step
    
    Args:
        prompt_name: Name of the prompt file
        **kwargs: Variables to format into the template
    
    Returns:
        str: Loaded and formatted prompt
    """
    template = load_prompt(prompt_name)
    return format_prompt(template, **kwargs)
