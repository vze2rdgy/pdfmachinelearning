DROP FUNCTION IF EXISTS public.search(text, text);
CREATE OR REPLACE FUNCTION public.search(searchstring text, domain text)
    RETURNS TABLE(docid bigint, pn text, weightage text, incis character varying[], claims character varying[], filename text , supplier text ) AS $$
DECLARE
	temp text;	
BEGIN
	temp := '%' || searchstring || '%';
	RETURN query select DISTINCT ON (a."DocId") a."DocId" as docid, left(b.pn,150), '0'::text as weightage, c.incis, d.claims,e."FilePath"::text as filename, 'Supplier name'::text as supplier from "DocMetaData" a 
	join (select DISTINCT ON ("DocId") "DocId", "TagData"  from "DocMetaData" where lower("TagData") like lower(temp) ) f
		on a."DocId" = f."DocId"
	left join (select DISTINCT ON ("DocId") "DocId", "TagData" as "pn" from "DocMetaData" where "TagId" = 37) b 
		on a."DocId" = b."DocId"
	left join (select "DocId", array_agg("TagData") as "incis" from "DocMetaData" where "TagId" = 38 group by "DocId") c
		on a."DocId" = c."DocId"
	left join (select "DocId", array_agg("TagData") as "claims" from (
					select "DocId", "TagData", rank() over(partition by "DocId" order by "TagData") as "rank" from "DocMetaData" where "TagId" = 16 ) claims
				where rank <=3 group by "DocId" ) d
		on a."DocId" = d."DocId"
 	left join "Documents" e
        on a."DocId" = e."DocId";		
END; 
$$ LANGUAGE plpgsql;
ALTER FUNCTION public.search(text, text)
    OWNER TO iclapuser;

select docid, pn, weightage, incis, claims,filename, supplier from  public.search('water', 'skin');

