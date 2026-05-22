#!/bin/bash
# Get all user URLs

echo "============================================"
echo "Workshop User URLs"
echo "============================================"
echo ""

oc get routes -A | grep "comparison-ui" | while read -r line; do
    ROUTE_NAME=$(echo "$line" | awk '{print $2}')
    HOST=$(echo "$line" | awk '{print $3}')

    echo "https://${HOST}"
done

echo ""
echo "============================================"
echo "Total users: $(oc get routes -A | grep -c 'comparison-ui')"
echo "============================================"
