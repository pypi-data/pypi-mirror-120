from django.test import SimpleTestCase
from django.template import Context, Template


class CreateDsfrCssTagTest(SimpleTestCase):
    def test_css_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %} {% dsfr_css %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            '<link rel="stylesheet" href="/static/dsfr/dist/css/dsfr.min.css">',
            rendered_template,
        )


class CreateDsfrJsTagTest(SimpleTestCase):
    def test_js_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %} {% dsfr_js %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
<script type="module" src="/static/dsfr/dist/js/dsfr.module.min.js"></script>
<script type="text/javascript" nomodule src="/static/dsfr/dist/js/dsfr.nomodule.min.js"></script>""",
            rendered_template,
        )


class CreateDsfrFaviconTagTest(SimpleTestCase):
    def test_favicon_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %} {% dsfr_favicon %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
<link rel="apple-touch-icon" href="/static/dsfr/dist/favicons/apple-touch-icon.png"><!-- 180×180 -->
<link rel="icon" href="/static/dsfr/dist/favicons/favicon.svg" type="image/svg+xml">
<link rel="shortcut icon" href="/static/dsfr/dist/favicons/favicon.ico" type="image/x-icon">
<!-- 32×32 -->
<link rel="manifest" href="/static/dsfr/dist/favicons/manifest.webmanifest"
crossorigin="use-credentials">""",
            rendered_template,
        )


class CreateDsfrThemeModaleTagTest(SimpleTestCase):
    def test_theme_modale_tag_rendered(self):
        context = Context()
        template_to_render = Template("{% load dsfr_tags %} {% dsfr_theme_modale %}")
        rendered_template = template_to_render.render(context)
        self.assertInHTML(
            """
                        <h1 id="fr-theme-modal-title" class="fr-modal__title">
                            Paramètres d’affichage
                        </h1>""",
            rendered_template,
        )


class CreateDsfrAccordionTagTest(SimpleTestCase):
    test_data = {
        "id": "sample-accordion",
        "title": "Title of the accordion item",
        "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template("{% load dsfr_tags %} {% dsfr_accordion test_data %}")

    def test_accordion_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
<section class="fr-accordion">
    <h3 class="fr-accordion__title">
        <button class="fr-accordion__btn" aria-expanded="false" aria-controls="sample-accordion">Title of the accordion item</button>
    </h3>
    <div class="fr-collapse" id="sample-accordion">
        <p><b>Bold</b> and <em>emphatic</em> Example content</p>
    </div>
</section>
""",
            rendered_template,
        )


class CreateDsfrAccordionGroupTagTest(SimpleTestCase):
    test_data = [
        {
            "id": "sample-accordion",
            "title": "Title of the accordion item",
            "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
        },
        {
            "id": "sample-accordion-2",
            "title": "Title of the second accordion item",
            "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
        },
        {
            "id": "sample-accordion-3",
            "title": "Title of the third accordion item",
            "content": "<p><b>Bold</b> and <em>emphatic</em> Example content</p>",
        },
    ]

    context = Context({"test_data": test_data})
    template_to_render = Template(
        "{% load dsfr_tags %} {% dsfr_accordion_group test_data %}"
    )

    def test_accordion_group_count(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<p><b>Bold</b> and <em>emphatic</em> Example content</p>""",
            rendered_template,
            count=3,
        )


class CreateDsfrAlertTagTest(SimpleTestCase):
    test_data = {
        "title": "Sample title",
        "type": "info",
        "content": "Sample content",
        "heading_tag": "h3",
        "is_collapsible": True,
        "id": "test-alert-message",
    }

    context = Context({"test_data": test_data})
    template_to_render = Template("{% load dsfr_tags %} {% dsfr_alert test_data %}")

    def test_alert_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML("""<p>Sample content</p>""", rendered_template)

    def test_alert_tag_heading_can_be_set(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<h3 class="fr-alert__title">Sample title</h3>""", rendered_template
        )

    def test_alert_tag_has_collapse_button(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
<button class="fr-link--close fr-link" aria-expanded="true" aria-controls="test-alert-message">
    Masquer le message
</button>""",
            rendered_template,
        )


class CreateDsfrBreadcrumbTagTest(SimpleTestCase):
    breadcrumb_data = {
        "links": [{"url": "test-url", "title": "Test title"}],
        "current": "Test page",
    }

    context = Context({"breadcrumb_data": breadcrumb_data})
    template_to_render = Template(
        "{% load dsfr_tags %} {% dsfr_breadcrumb breadcrumb_data %}"
    )

    def test_breadcrumb_tag_current_page(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<a class="fr-breadcrumb__link" aria-current="page">Test page</a>""",
            rendered_template,
        )

    def test_breadcrumb_tag_middle_link(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<a class="fr-breadcrumb__link" href="test-url">Test title</a>""",
            rendered_template,
        )


class CreateDsfrCalloutTagTest(SimpleTestCase):
    callout_data = {
        "text": "Text of the callout item",
        "title": "Title of the callout item",
        "icon_class": "fr-fi-information-line",
        "button": {"onclick": "close()", "label": "button label"},
    }

    context = Context({"callout_data": callout_data})
    template_to_render = Template(
        "{% load dsfr_tags %} {% dsfr_callout callout_data %}"
    )

    def test_callout_tag_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
    <p class="fr-callout__text">
        Text of the callout item
    </p>""",
            rendered_template,
        )

    def test_callout_optional_title_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """<h4 class="fr-callout__title">Title of the callout item</h4>""",
            rendered_template,
        )

    def test_callout_optional_icon_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue("fr-fi-information-line" in rendered_template)

    def test_callout_optional_button_rendered(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
    <button
        class="fr-btn"
        onclick="close()"
    >
        button label
    </button>""",
            rendered_template,
        )


class CreateDsfrCardTagTest(SimpleTestCase):
    card_data = {
        "detail": "Appears before the title of the card item",
        "title": "Title of the card item",
        "description": "Text of the card item",
        "image_url": "https://test.gouv.fr/test.png",
    }

    extra_classes = "test-extraclass"
    new_tab = True

    context = Context(
        {"card_data": card_data, "extra_classes": extra_classes, "new_tab": new_tab}
    )
    template_to_render = Template(
        "{% load dsfr_tags %} {% dsfr_card card_data extra_classes=extra_classes new_tab=newtab %}"
    )

    def test_card_is_created(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertTrue("fr-card" in rendered_template)

    def test_card_has_detail(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            '<p class="fr-card__detail">Appears before the title of the card item</p>',
            rendered_template,
        )

    def test_card_has_title(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
                <p class="fr-card__title">
                <a href="" class="fr-card__link" target="_self">
                    Title of the card item
                </a>
            </p>""",
            rendered_template,
        )

    def test_card_has_description(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            '<p class="fr-card__desc">Text of the card item</p>',
            rendered_template,
        )

    def test_card_has_optional_image(self):
        rendered_template = self.template_to_render.render(self.context)
        self.assertInHTML(
            """
    <div class="fr-card__img">
        <img src="https://test.gouv.fr/test.png" class="fr-responsive-img" alt="">
    </div>""",
            rendered_template,
        )
