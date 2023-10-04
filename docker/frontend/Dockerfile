# FROM node:alpine

# WORKDIR /app/frontend
# # ADD ./frontend /app/frontend/
# ADD ./frontend .

# RUN npm install

# RUN npm run build

# EXPOSE 3000

# CMD [ "npm", "start" ]
# ######################################################

# FROM node:18-alpine AS deps
# RUN apk add --no-cache libc6-compat
# WORKDIR /app/frontend

# COPY frontend/package.json frontend/package-lock.json ./
# RUN  npm install --production

# FROM node:18-alpine AS builder
# WORKDIR /app/frontend
# COPY --from=deps /app/frontend/node_modules ./node_modules
# COPY ./frontend/ .

# ENV NEXT_TELEMETRY_DISABLED 1

# RUN npm run build

# FROM node:18-alpine AS runner
# WORKDIR /app/frontend

# ENV NODE_ENV production
# ENV NEXT_TELEMETRY_DISABLED 1

# RUN addgroup --system --gid 1001 nodejs
# RUN adduser --system --uid 1001 nextjs

# COPY --from=builder --chown=nextjs:nodejs /app/frontend/.next ./.next
# COPY --from=builder /app/frontend/public ./public
# COPY --from=builder /app/frontend/node_modules ./node_modules
# COPY --from=builder /app/frontend/package.json ./package.json

# USER nextjs

# EXPOSE 3000

# ENV PORT 3000

# CMD ["npm", "start"]


FROM node:18-alpine AS base

# 1. Install dependencies only when needed
FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Install dependencies based on the preferred package manager
COPY frontend/package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi

# 2. Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# This will do the trick, use the corresponding env file for each environment.
COPY .env.development.sample .env.production
RUN yarn build

# 3. Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static


USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME localhost

CMD ["node", "server.js"]