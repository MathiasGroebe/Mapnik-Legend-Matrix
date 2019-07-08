UPDATE mapnik_styles
SET RuleMinScale = 1
WHERE RuleMinScale IS NULL OR RuleMinScale = '';
UPDATE mapnik_styles
SET LayerMinScale = 1
WHERE LayerMinScale IS NULL OR RuleMinScale = '';
UPDATE mapnik_styles
SET RuleMaxScale = 1000000000
WHERE RuleMaxScale IS NULL OR RuleMaxScale = '';
UPDATE mapnik_styles
SET LayerMaxScale = 1000000000
WHERE LayerMaxScale IS NULL OR RuleMaxScale = '';