FROM ubuntu:22.04

# Avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install PostgreSQL server and client
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Postgres creates a 'postgres' user automatically during installation.
# Let's set up the data directory and give that user ownership.
RUN mkdir -p /var/lib/postgresql/data /var/run/postgresql \
    && chown 1000:1000 /var/lib/postgresql/data /var/run/postgresql

# Update PATH so the system can find 'initdb' and 'postgres' commands easily
ENV PATH="/usr/lib/postgresql/14/bin:$PATH"

# ADD THIS LINE: Explicitly direct Postgres to use a subfolder inside the volume.
# This ensures initdb owns the directory completely and can change internal permissions.
ENV PGDATA="/var/lib/postgresql/data/pgdata"

# Copy our entrypoint config script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the standard Postgres port
EXPOSE 5432

# Switch away from root to the standard postgres user for security
# USER postgres

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]