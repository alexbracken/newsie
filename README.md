# Newsie
A barebones, no-nonsense Python script for posting news stories to social media platforms. Designed for simplicity, ease of use, and cost-effectiveness, so journalists can focus on reporting.

  _Currently under active development. This script may or may not work and has not been tested extensively._

## Dependencies
- Python (tested on 3.14)
- Poetry (dependency management)
    - View pyproject.toml for full dependencies

## Setup
- _Coming soon_

## References
### Meta GraphAPI
- [GraphAPI Page Feed Reference](https://developers.facebook.com/docs/graph-api/reference/v21.0/page/feed)
- [GraphAPI Photo Reference](https://developers.facebook.com/docs/graph-api/reference/page/photos/#upload)

### RSS Feeds
- [BLOX CMS RSS Documentation](https://www.help.bloxdigital.com/blox_cms/faq/how-to-generate-rss-mrss-atom-and-iatom-feeds-from-blox/article_1518c53a-c099-59a0-bbc2-446c11ad043b.html)

### Python Graph API Wrapper (pyfacebook)
- [Documentation](https://sns-sdks.lkhardy.cn/python-facebook/usage/graph-api/)
- [Examples](https://github.com/sns-sdks/python-facebook/tree/master/examples)

## TODO
- Error logging
- Debug mode
  - Need a way to test Facebook API connection without posting
- Comment link after posting photos
  - Gets around Facebook suppression of link posts

## Potential Enhancements
- Smart Slots
    - Calculate engagement rates by time, concentrate slots based on that model
- AI-enhanced captions
    - Use locally-hosted LLM or API key
- Interactive CLI setup
