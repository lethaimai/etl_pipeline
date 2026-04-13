{%macro user_rating_bucket(col, excellent= 4.5, good= 4.0, average= 3.0) -%}
case
    when {{col}} >= {{excellent}} then 'Excellent'
    when {{col}} >= {{good}} then 'Good'
    when {{col}} >= {{average}} then 'Average'
    else 'Poor'
end
{%- endmacro -%}



