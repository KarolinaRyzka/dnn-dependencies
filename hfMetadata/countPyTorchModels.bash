#!/bin/bash
jq -r ".[].siblings[].rfilename" hf_metadata.json | grep -E "\.pth\b|\.pt\b" | wc -l
