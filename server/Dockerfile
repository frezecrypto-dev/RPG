# Ashgate API — zero-dependency Node server.
FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /app

# No dependencies to install: the server is stdlib-only. Copying package.json
# first keeps the layer cache useful if that ever changes.
COPY package.json ./
COPY *.js ./

# Saves live outside the image so a redeploy doesn't wipe them.
ENV ASHGATE_DB=/data/db.json
RUN mkdir -p /data && chown -R node:node /data /app
USER node

EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- "http://127.0.0.1:${PORT:-8787}/health" || exit 1

CMD ["node", "index.js"]
