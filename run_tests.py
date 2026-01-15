#!/usr/bin/env python
"""
Quick test runner for the Lead Capture Agent pipeline
This validates that all components work end-to-end
"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.tests.test_lead_flow import test_pipeline
    test_pipeline()
