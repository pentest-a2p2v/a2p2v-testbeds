# README


Requirements

- Flask
- pymodbus

## Background

There are four register in the PLC

- Tag
- Temperature (Read-only)
- Setting (Read-Write)
- Control

## Usage

Install requirements:

    pip install -r requirements

Execute the web server:

    python -m flaskhmi
