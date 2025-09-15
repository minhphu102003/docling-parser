module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'body-max-line-length': [0, 'always', 100], // Disable body max line length
    'footer-max-line-length': [0, 'always', 100], // Disable footer max line length
  },
};