SELECT
    *
FROM(
    SELECT
      uma.surface AS uma_surface,
      uma.pos AS uma_pos,
      uma.pos1 AS uma_pos1,
      uma.pos2 AS uma_pos2,
      uma.pos3 AS uma_pos3,
      uma.ctype AS uma_ctype,
      uma.cform AS uma_cform,
      uma.base AS uma_base,
      uma.yomi AS uma_yomi,
      uma.pron AS uma_pron,
      m.morpheme_id AS m_morpheme_id
    FROM (
      SELECT
        morphemes.surface AS surface,
        morphemes.pos AS pos,
        morphemes.pos1 AS pos1,
        morphemes.pos2 AS pos2,
        morphemes.pos3 AS pos3,
        morphemes.ctype AS ctype,
        morphemes.cform AS cform,
        morphemes.base AS base,
        morphemes.yomi AS yomi,
        morphemes.pron AS pron
      FROM
        morphemes
      GROUP BY
        morphemes.surface,
        morphemes.pos,
        morphemes.pos1,
        morphemes.pos2,
        morphemes.pos3,
        morphemes.ctype,
        morphemes.cform,
        morphemes.base,
        morphemes.yomi,
        morphemes.pron
    ) AS uma
    LEFT OUTER JOIN (
        SELECT
          morpheme_dictionary.morpheme_dict_id AS morpheme_id,
          morpheme_dictionary.surface AS surface,
          morpheme_dictionary.pos AS pos,
          morpheme_dictionary.pos1 AS pos1,
          morpheme_dictionary.pos2 AS pos2,
          morpheme_dictionary.pos3 AS pos3,
          morpheme_dictionary.ctype AS ctype,
          morpheme_dictionary.cform AS cform,
          morpheme_dictionary.base AS base,
          morpheme_dictionary.yomi AS yomi,
          morpheme_dictionary.pron AS pron
        FROM
          morpheme_dictionary
    )AS m
    ON  ((uma.surface = m.surface) OR (uma.surface IS NULL AND m.surface IS NULL))
    AND ((uma.pos = m.pos) OR (uma.pos IS NULL AND m.pos IS NULL))
    AND ((uma.pos1 = m.pos1) OR (uma.pos1 IS NULL AND m.pos1 IS NULL))
    AND ((uma.pos2 = m.pos2) OR (uma.pos2 IS NULL AND m.pos2 IS NULL))
    AND ((uma.pos3 = m.pos3) OR (uma.pos3 IS NULL AND m.pos3 IS NULL))
    AND ((uma.ctype = m.ctype) OR (uma.ctype IS NULL AND m.ctype IS NULL))
    AND ((uma.cform = m.cform) OR (uma.cform IS NULL AND m.cform IS NULL))
    AND ((uma.base = m.base) OR (uma.base IS NULL AND m.base IS NULL))
    AND ((uma.yomi = m.yomi) OR (uma.yomi IS NULL AND m.yomi IS NULL))
    AND ((uma.pron = m.pron ) OR (uma.pron IS NULL AND m.pron IS NULL))
) AS a
WHERE
    m_morpheme_id IS NULL
LIMIT 5
