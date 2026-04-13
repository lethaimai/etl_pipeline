
  
    

  create  table "destination_db"."public"."specific_movie__dbt_tmp"
  
  
    as
  
  (
    SELECT *
FROM films
WHERE rating = 'PG-13'
  );
  