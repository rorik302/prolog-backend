from alembic.script import ScriptDirectory


def alembic_include_object():
    def include_object(object_, name, type_, reflected, compare_to):
        if type_ == "foreign_key_constraint":
            return False

        return True

    return include_object


def alembic_process_revision_directives(config, context):
    def process_revision_directives(context_, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

            head_revision = ScriptDirectory.from_config(context.config).get_current_head()

            if head_revision is None:
                new_rev_id = 1
            else:
                last_rev_id = int(head_revision.lstrip("0"))
                new_rev_id = last_rev_id + 1
            script.rev_id = f"{new_rev_id:04}"

    return process_revision_directives
