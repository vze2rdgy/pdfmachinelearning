
-- FUNCTION: public.products(bigint)

-- DROP FUNCTION public.products(bigint);

CREATE OR REPLACE FUNCTION public.products(
	searchproduct bigint)
    RETURNS TABLE(docid bigint, pn text, weightage text, incis character varying[], claims character varying[], filename text , supplier text) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$DECLARE
	temp bigint;	
BEGIN
	--temp := regexp_split_to_array(searchstring, ' ');
	temp :=  searchproduct  ;
	RETURN query select DISTINCT ON (a."DocId") a."DocId" as docid, left(b.pn,150), '0'::text as weightage, c.incis, d.claims, e."FilePath"::text as filename, 'Supplier name'::text as supplier 
	from "DocMetaData" a 
	join (select DISTINCT ON ("DocId") INDM."DocId"
		  from "DocMetaData"  INDM
		  inner join  "Documents"   INDOC
		  ON INDM."DocId"  = INDOC."DocId" 
		  and INDOC."SupplId"  = temp
		  ) f
	on a."DocId" = f."DocId"
	
	left join (select DISTINCT ON ("DocId") "DocId", "TagData" as "pn" from "DocMetaData" where "TagId" = 37) b 
		on a."DocId" = b."DocId"
	
	left join (select "DocId", array_agg("TagData") as "incis" from "DocMetaData" where "TagId" = 38 group by "DocId") c
		on a."DocId" = c."DocId"
	
	left join (select "DocId", array_agg("TagData") as "claims" from (
					select "DocId", "TagData", rank() over(partition by "DocId" order by "TagData") as "rank" from "DocMetaData" where "TagId" = 16 ) claims
				where rank <=6 group by "DocId" ) d
		on a."DocId" = d."DocId"
 	left join "Documents" e
        on a."DocId" = e."DocId";
END; 
$BODY$;

ALTER FUNCTION public.products(bigint)
    OWNER TO iclapuser;