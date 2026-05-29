-- summary.sql
-- Top 10 news sources by article count for the tracked query term,
-- over the last 7 days. Shows which sources dominate coverage.

SELECT
    source_name,
    source_domain,
    COUNT(*)                                          AS article_count,
    ROUND(AVG(title_word_count), 1)                  AS avg_title_words,
    COUNTIF(has_description = TRUE)                  AS articles_with_description,
    ROUND(
        COUNTIF(has_description = TRUE) * 100.0 / COUNT(*), 1
    )                                                AS pct_with_description,
    MIN(published_at)                                AS earliest_article,
    MAX(published_at)                                AS latest_article
FROM
    `your-project-id.news_pipeline.articles`
WHERE
    ingested_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
    AND source_name IS NOT NULL
GROUP BY
    source_name,
    source_domain
ORDER BY
    article_count DESC
LIMIT 10;
