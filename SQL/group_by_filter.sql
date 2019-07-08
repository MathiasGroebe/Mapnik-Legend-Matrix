SELECT RuleFilterEdit
FROM mapnik_styles 
WHERE StyleName = 'buildings'
GROUP BY  RuleFilterEdit
ORDER BY RuleFilterEdit