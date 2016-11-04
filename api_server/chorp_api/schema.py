from graphene import ObjectType, relay, AbstractType, Mutation
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
import graphene
from .models import Booking, Pet, PetType, Task
from graphene_django.debug import DjangoDebug


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        filter_fields = ['id', 'username']


class BookingNode(DjangoObjectType):
    class Meta:
        model = Booking
        interfaces = (relay.Node, )


class PetNode(DjangoObjectType):
    class Meta:
        model = Pet
        interfaces = (relay.Node, )


class PetTypeNode(DjangoObjectType):
    class Meta:
        model = PetType
        interfaces = (relay.Node, )
        filter_fields = ['name']
        filter_order_by = ['name']


class TaskNode(DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (relay.Node, )


class TaskQueries(AbstractType):
    task = relay.Node.Field(TaskNode)
    tasks = DjangoFilterConnectionField(TaskNode)


class UserQueries(AbstractType):
    user = relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    @staticmethod
    def resolve_users(self, args, context, info):
        if not context.user.is_authenticated():
            return User.objects.none()
        elif context.user.has_perm('chorp.admin'):
            return User.objects.all()
        else:
            return User.objects.filter(id=context.user.id)


class PetQueries(AbstractType):
    pet_type = relay.Node.Field(PetTypeNode)
    pet_types = DjangoFilterConnectionField(PetTypeNode)

    pet = relay.Node.Field(PetNode)
    pets = DjangoFilterConnectionField(PetNode)


class BookingQueries(AbstractType):
    booking = relay.Node.Field(BookingNode)
    bookings = DjangoFilterConnectionField(BookingNode)


class Queries(UserQueries, PetQueries, BookingQueries, TaskQueries, ObjectType):
    node = relay.Node.Field()
    debug = graphene.Field(DjangoDebug, name='__debug')


class CreateTask(Mutation):
    class Input:
        title = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    task = graphene.Field(TaskNode)

    @classmethod
    def mutate(self, args, context, info, fifth):
        task = Task(title=context.get('title'), description=context.get('description'))
        ok = True
        return CreateTask(task=task, ok=ok)


class Mutations(ObjectType):
    create_task = CreateTask.Field()


schema = graphene.Schema(query=Queries, mutation=Mutations)

'''
Sample queries.

- Query
{
  petTypes {
    edges {
      node {
        id
        name
      }
    }
  }
}
- Result
{
  "data": {
    "petTypes": {
      "edges": [
        {
          "node": {
            "id": "UGV0VHlwZU5vZGU6Mg==",
            "name": "Cat"
          }
        },
        {
          "node": {
            "id": "UGV0VHlwZU5vZGU6MQ==",
            "name": "Dog"
          }
        }
      ]
    }
  }
}

- Query
{
  petType(id: "UGV0VHlwZU5vZGU6Mg==") {
    name
  }
}
- Result
{
  "data": {
    "petType": {
      "name": "Cat"
    }
  }
}
'''
