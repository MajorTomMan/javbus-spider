#!/bin/bash
gnome-terminal -- bash -c "scrapy crawl movie; exec bash"
gnome-terminal -- bash -c "scrapy crawl actress_detail; exec bash"
gnome-terminal -- bash -c "scrapy crawl actress_movie; exec bash"