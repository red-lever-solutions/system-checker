#!/bin/sh

curl http://192.168.99.100:8080/api/v0.1/4c0590d88ff3460d92f4b78714b2c393/tileconfig/service-checker-tile \
     -X POST \
     -d 'value={"vertical_center": true,
                "1": {"label_color": "red"},
                "2": {"label_color": "red"},
                "3": {"label_color": "green"}}'

curl http://192.168.99.100:8080/api/v0.1/4c0590d88ff3460d92f4b78714b2c393/push \
     -X POST \
     -d "tile=scrollable_fancy_listing" \
     -d "key=service-checker-tile" \
     -d 'data=[{"label": "My label 1", "text": "Lorem ipsum", "description": "such description" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 2", "text": "Dolor sit", "description": "yet another" },
               {"label": "My label 3", "text": "Amet", "description": "" }]'
