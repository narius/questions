SELECT tags.id, tags.text, count(questions.id) AS number_of_questions FROM tags
LEFT JOIN question_tags ON tags.id=question_tags.tag_id
LEFT JOIN questions ON question_tags.question_id=questions.id
GROUP BY tags.id
ORDER BY tags.text