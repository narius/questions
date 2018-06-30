SELECT questions.id, questions.text AS text, STRING_AGG(tags.text, ',') AS tags, count(votes.id) AS votes, count(question_tags.id) AS n_tags FROM questions 
JOIN votes ON votes.question_id=questions.id
LEFT JOIN question_tags on question_tags.question_id=questions.id
LEFT JOIN tags on tags.id=question_tags.tag_id
GROUP BY questions.id
ORDER BY count(votes.id) DESC