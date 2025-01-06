# services/nginx/Dockerfile
FROM nginx:latest

# Copy the NGINX configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Install necessary tools
RUN apt-get update && apt-get install -y procps

# Create directories for static files and default HTML files
RUN mkdir -p /usr/share/nginx/html && \
    echo "<html><head><title>Learn2Learn</title></head><body><h1>Welcome to Learn2Learn!</h1></body></html>" > /usr/share/nginx/html/index.html && \
    if [ ! -f /usr/share/nginx/html/404.html ]; then \
        echo "<html><head><title>404 Not Found</title></head><body><h1>404 - Page Not Found</h1></body></html>" > /usr/share/nginx/html/404.html; \
    fi && \
    if [ ! -f /usr/share/nginx/html/50x.html ]; then \
        echo "<html><head><title>50x Error</title></head><body><h1>50x - Server Error</h1></body></html>" > /usr/share/nginx/html/50x.html; \
    fi

# Create directories for SSL certificates
RUN mkdir -p /etc/ssl/nginx/certs /etc/ssl/nginx/private && \
    chmod 700 /etc/ssl/nginx/private

# Expose ports for HTTP and HTTPS
EXPOSE 80 443

# Set NGINX to run in the foreground
CMD ["nginx", "-g", "daemon off;"]
