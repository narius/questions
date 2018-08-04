SELECT questions.id, questions.text AS text, STRING_AGG(DISTINCT tags.text, ',') AS tags_text, count(votes.id) AS votes FROM questions 
INNER JOIN votes ON votes.question_id=questions.id
LEFT JOIN question_tags on question_tags.question_id=questions.id
LEFT JOIN tags on tags.id=question_tags.tag_id
GROUP BY questions.id
ORDER BY count(votes.id) DESC