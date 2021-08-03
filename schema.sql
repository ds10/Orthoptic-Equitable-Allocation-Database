<?xml version="1.0" encoding="UTF-8" ?>
<project name="orthoptic_equtable" id="Project_1bdf" database="Sqlite" >
	<schema name="Default" >
		<table name="Group" prior="Tbl" >
			<column name="GroupID" type="integer" jt="4" mandatory="y" />
			<column name="Name" type="varchar" length="100" jt="12" />
			<index name="Pk_Tbl_GroupID" unique="PRIMARY_KEY" >
				<column name="GroupID" />
			</index>
		</table>
		<table name="Location" prior="location" >
			<column name="LocationID" prior="id" type="integer" jt="4" mandatory="y" />
			<column name="GroupID" prior="group_id" type="integer" jt="4" />
			<column name="Longname" prior="longname" type="varchar" length="100" jt="12" />
			<column name="Shortname" prior="shortname" type="varchar" length="100" jt="12" />
			<index name="Pk_locations_id" unique="PRIMARY_KEY" >
				<column name="LocationID" />
			</index>
			<fk name="Fk_Location" to_schema="Default" to_table="Preferences" >
				<fk_column name="LocationID" pk="LocationID" />
			</fk>
			<fk name="Fk_Location_0" to_schema="Default" to_table="Group" >
				<fk_column name="GroupID" pk="GroupID" />
			</fk>
		</table>
		<table name="Preferences" >
			<column name="PreferenceID" type="integer" jt="4" mandatory="y" />
			<column name="LocationID" type="integer" jt="4" />
			<column name="Universities" type="varchar" length="255" jt="12" />
			<column name="Years" type="varchar" length="255" jt="12" />
			<column name="Capacity" type="decimal" length="127" jt="3" />
			<column name="WTE" type="double" length="10" decimal="10" jt="8" />
			<column name="EquitableAllocation" prior="Allocation" type="double" jt="8" />
			<column name="SugguestedAllocation" prior="Sugguested" type="double" jt="8" />
			<column name="AgreedAllocation" prior="Agreed" type="double" jt="8" />
			<column name="EquitableAgreed" prior="Equitable_Agreed" type="double" jt="8" />
			<index name="Pk_Preferences_PreferenceID" unique="PRIMARY_KEY" >
				<column name="PreferenceID" />
			</index>
			<index name="Unq_Preferences_LocationID" unique="UNIQUE_KEY" >
				<column name="LocationID" />
			</index>
		</table>
		<table name="University" prior="universities" >
			<column name="UniversityID" type="integer" jt="4" mandatory="y" />
			<column name="Name" type="varchar" length="100" jt="12" />
			<index name="Pk_universities_UniversityID" unique="PRIMARY_KEY" >
				<column name="UniversityID" />
			</index>
		</table>
	</schema>
	<layout name="Default Layout" id="Layout_e7c" show_relation="columns" >
		<entity schema="Default" name="Group" color="C1D8EE" x="496" y="48" />
		<entity schema="Default" name="Location" color="C1D8EE" x="176" y="48" />
		<entity schema="Default" name="Preferences" color="C1D8EE" x="48" y="272" />
		<callout x="576" y="464" pointer="Round" >
			<comment><![CDATA[DbSchema is disconnected from the database.
New designed tables will be saved to project file and later can be create in any database.
Right-click the layout to create new tables. Drop this callout from its context menu.]]></comment>
		</callout>
		<script name="SQL_Editor" id="Editor_7aa" language="SQL" >
			<string><![CDATA[CREATE TABLE location ( 
	id                   integer NOT NULL  PRIMARY KEY  ,
	group_id             integer     ,
	longname             varchar(100)     ,
	shortname            varchar(100)     
 );
]]></string>
		</script>
	</layout>
</project>