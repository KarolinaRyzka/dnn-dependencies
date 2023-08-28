#!/bin/bash
jq -r ".[].siblings[].rfilename" hf_metadata.json | grep -E "\.pb" | wc -l
