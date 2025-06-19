#!/usr/bin/env python3
"""
🚀 Air Quality Monitor - Quick Start Script
Simple launcher for the Air Quality Index monitoring system
"""

import sys
import os
from config import Config

def main():
    """Main startup function"""
    print("🌍 Air Quality Index Monitor")
    print("=" * 40)
    
    try:
        # Validate configuration
        Config.validate_config()
        Config.display_config()
        print()
        
        print("📋 Available options:")
        print("1. 🌐 Web Interface (Gradio)")
        print("2. 💬 Command Line Chat")
        print("3. ❌ Exit")
        print()
        
        choice = input("👉 Choose an option (1-3): ").strip()
        
        if choice == "1":
            print("🚀 Starting web interface...")
            os.system("python web_interface.py")
        elif choice == "2":
            print("💬 Starting command line interface...")
            os.system("python function_calling.py")
        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")
            main()
            
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n🔧 Please check your .env file and ensure your API key is set correctly.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 