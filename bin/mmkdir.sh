#!/bin/bash
while [ ! -z "$1" ]; do
  mkdir -p "$1"
  shift
done
