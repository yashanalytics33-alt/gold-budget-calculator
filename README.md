# Gold Budget Calculator

An interactive jewellery pricing application built using Python and Streamlit that estimates the final cost of gold jewellery based on purity, weight, making charges, decoration costs, and applicable GST.

## Features
- Live gold price fetching using REST APIs
- Purity-based valuation (18K, 20K, 22K, 24K)
- Making charges and decoration cost calculation
- GST computation (CGST + SGST)
- Secure login using hashed credentials
- Fallback pricing logic during API downtime

## Tech Stack
- Python
- Streamlit
- REST APIs
- Requests
- Pillow

## How It Works
The application fetches live gold prices via an external API, processes pricing logic using business rules, and presents a detailed cost breakdown through an interactive user interface.

## Project Motivation
This project demonstrates the application of Python, APIs, and business logic to solve a real-world pricing and cost estimation problem in the jewellery domain.

## Note
API keys are not exposed in this repository and should be configured securely using environment variables or Streamlit secrets.

