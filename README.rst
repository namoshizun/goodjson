========
GoodJSON
========
GoodJSON gives a way of composing simple validator functions to build JSON validation workflows. You can easily define your own "building block" validators and combine them with GoodJSON's builtin validators to perform highly flexible and complex validations.


Installation
============
TODO

Usage
=====
TODO

.. code-block:: python
  :linenos:

  from goodjson import errors, types, decorators
  from goodjson.validators import foreach_key, foreach, is_string, is_list

  # Each custom validator must have a ErrorMessage
  prefix_not_found = errors.ErrorMessage(
      name='prefix_not_found',
      description='Expected prefix {prefix} is not found'
  )

  # Create a parameterizable custom validator
  def has_prefix_value(begin_value: str) -> types.ValidatorFunction:

      # "Validator" decorator adds error message to a simple checker function returning boolean
      @decorators.validator(prefix_not_found.format(prefix=begin_value))
      def checker(value: str) -> types.CheckerReturn:
          # ...
          # DO WHATEVER YOU WANT!
          return value.startswith(begin_value)

      return checker

  # ---------------------------------
  # Compose your validation blueprint
  is_good_json = foreach_key(
      codes=[
          is_list(),
          foreach(is_string, has_prefix_value('GJ_'))
      ]
  )

  ok, error = is_good_json({ 'codes': ['GJ_00001', '_00010'] })
  print(error)
  """
  Should print: 

  {
      "error": "Expected prefix GJ_ is not found",
      "data": {
          "path" : "_root_$codes$1",
          "value": "_00010"
      }
  }
  """



Examples
========
TODO

Coming up: v0.2.0
=================
Features to be added into the next version:

* Return all validation errors found instead of early quitting.
* Lazy application of validators.
* More higher order validators.
