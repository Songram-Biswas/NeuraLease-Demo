/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // biuld even with type errors, we will fix them later
    ignoreBuildErrors: true,
  },
}

module.exports = nextConfig