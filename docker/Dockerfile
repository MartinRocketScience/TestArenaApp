# Use PHP 7.2 with Apache as the base image
FROM php:7.2-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    default-mysql-client

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd mysqli

# Enable Apache modules
RUN a2enmod rewrite

# Configure PHP
COPY php.ini /usr/local/etc/php/php.ini

# Set working directory
WORKDIR /var/www/html

# Copy application files
COPY TastArenaApp/ /var/www/html/

# Configure Apache
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/html/public\n\
    <Directory /var/www/html/public>\n\
        Options Indexes FollowSymLinks\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
    ErrorLog /dev/stderr\n\
    CustomLog /dev/stdout combined\n\
    php_flag display_errors on\n\
    php_flag display_startup_errors on\n\
    php_value error_reporting E_ALL\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Set permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 777 /var/www/html/public/upload \
    && chmod -R 777 /var/www/html/public/captcha \
    && chmod -R 777 /var/www/html/logs \
    && chmod -R 777 /var/www/html/cache \
    && chmod -R 777 /var/www/html/temp

# Apache configuration
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Expose port 80
EXPOSE 80

# Start Apache in foreground
CMD ["apache2-foreground"]
