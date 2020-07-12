
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User
from .models import Grabit

# Graphene will automatically map the Grabit model's fields onto the GrabitNode.
# This is configured in the GrabitNode's Meta class (as you can see below)
class GrabitNode(DjangoObjectType):
    class Meta:
        model = Grabit
        filter_fields = ['creation_date', 'update_date']
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    grabit = graphene.relay.Node.Field(GrabitNode)
    all_grabits = DjangoFilterConnectionField(GrabitNode)

class CreateGrabit(graphene.relay.ClientIDMutation):
    msg = graphene.String()
    grabit = graphene.Field(GrabitNode)

    class Input:
        name = graphene.String(required=True)
        description = graphene.String()
        creation_date = graphene.DateTime()
        update_date = graphene.DateTime()
        graph = graphene.String()
        owner = graphene.String()


    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        
        name = input.get("name")
        owner = input.get("owner")
        try:
            user_owner = User.objects.get(pk=int(owner))

            new_grabit, created = Grabit.objects.update_or_create(name=name, owner=user_owner)

            msg = f"Created new grabit {name}" if created else f"Updated grabit {name}"

            return CreateGrabit(msg=msg, grabit=new_grabit)

        except Exception as e: 
            print(f"Error when creating or updating grabit {name}. {e}", flush=True)
            return CreateGrabit(msg=f"Can't create or update grabit {name}")

        #grabit.save()


class DeleteGrabit(graphene.relay.ClientIDMutation):
    msg = graphene.Field(type=graphene.String)
    grabit = graphene.Field(GrabitNode)

    class Input:
        name = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        obj = Grabit.objects.get(name=input["name"])
        try:
            obj.delete()
            msg = "Successful delete project {}".format(input["name"])
        except:
            msg = "Can't delete project {}".format(input["name"])
        print(msg)
        return DeleteGrabit(msg=msg, grabit=obj)


class Mutation(graphene.AbstractType):
    create_grabit = CreateGrabit.Field()
    delete_grabit = DeleteGrabit.Field()
