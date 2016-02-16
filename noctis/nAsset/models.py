from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class nObjectType(models.Model):
	"""
	What are we actually using when it comes to the nAsset
	"""
	
	name = models.CharField(max_length=150, default="")

	@python_2_unicode_compatible
	def __str__(self):
		return self.name

class nAsset(models.Model):
	"""
	The main object for any form of singular object component management
	in the pipeline. (i.e. a Render, 3D Model, Project File, Scripts, etc.)

	This bad boy has the potential to be both amazing and dangerous.
	When working on this there has to be a strong understanding of
	where the data may be pointing/queried from. For a baseline the
	Asset should rely off of three basic points...
	0=> The Real Object Pointer - The actual location of the data/thing
	1=> The Object Type - What is that object made of
	2=> The Object Relationship(s) - Where does this tie to other elements

	The last of that being the most ambiguous.
	
	Other elements can include things such as pointers to objects that are
	used to handle this asset. Whatever you see fit of course.
	"""
	
	# For basic simplicity we'll use a filepath but something
	# else can be used to replace this.
	name = models.CharField(max_length=150, default="")
	object_pointer = models.CharField(max_length=300, default="")
	object_type = models.ForeignKey(nObjectType, on_delete=models.CASCADE)

	## For a good basic relationship between iterations we're going to let
	## version control be delt with inter-asset-wise
	version = models.IntegerField(default=0)
	version_group_id = models.IntegerField(default=0)

	@python_2_unicode_compatible
	def __str__(self):
		return self.namephoto
