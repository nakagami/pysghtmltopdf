import unittest

import sghtmltopdf
from sghtmltopdf.options import to_argv


class TestOptions(unittest.TestCase):
    def test_to_argv_empty(self):
        argv = to_argv({})
        self.assertEqual(argv, [])

    def test_to_argv_flags(self):
        argv = to_argv({
            "page_size": "A4",
            "orientation": "Landscape",
            "grayscale": False,
            "margin_top": "10mm",
        })
        self.assertIn("--page-size", argv)
        self.assertIn("A4", argv)
        self.assertIn("--orientation", argv)
        self.assertIn("Landscape", argv)
        self.assertNotIn("--grayscale", argv)
        self.assertIn("--margin-top", argv)
        self.assertIn("10mm", argv)

    def test_to_argv_landscape_bool(self):
        argv = to_argv({"landscape": True})
        self.assertEqual(argv, ["--orientation", "Landscape"])

        argv = to_argv({"landscape": False})
        self.assertEqual(argv, ["--orientation", "Portrait"])

        argv = to_argv({"portrait": True})
        self.assertEqual(argv, ["--orientation", "Portrait"])

        argv = to_argv({"portrait": False})
        self.assertEqual(argv, ["--orientation", "Landscape"])

    def test_to_argv_list(self):
        argv = to_argv({"allow": ["/path/a", "/path/b"]})
        self.assertEqual(
            argv,
            [
                "--allow-path",
                "/path/a",
                "--allow-path",
                "/path/b",
            ],
        )

    def test_to_argv_font_dict(self):
        argv = to_argv({"font": {"path": "test.ttc", "index": 2}})
        self.assertEqual(
            argv,
            [
                "--font",
                "test.ttc",
                "--font-index",
                "2",
            ],
        )

    def test_to_argv_generic_font_dict(self):
        argv = to_argv({"gothic_font": {"path": "gothic.ttc", "index": 1}})
        self.assertEqual(
            argv,
            [
                "--gothic-font",
                "gothic.ttc",
                "--gothic-font-index",
                "1",
            ],
        )

    def test_to_argv_replace_dict(self):
        argv = to_argv({"replace": {"title": "My Title", "date": "2026-01-01"}})
        self.assertEqual(
            argv,
            [
                "--replace",
                "title=My Title",
                "--replace",
                "date=2026-01-01",
            ],
        )

    def test_to_argv_replace_tuple_list(self):
        argv = to_argv({"replace": [("[page]", "1"), ("[topage]", "10")]})
        self.assertEqual(
            argv,
            [
                "--replace",
                "[page]=1",
                "--replace",
                "[topage]=10",
            ],
        )


class TestRender(unittest.TestCase):
    def test_render_simple_html(self):
        html = "<html><body><h1>Hello World</h1><p>Test PDF generation</p></body></html>"
        pdf_data = sghtmltopdf.render(html)
        self.assertTrue(pdf_data.startswith(b"%PDF-"))
        self.assertGreater(len(pdf_data), 100)

    def test_render_with_options(self):
        html = "<html><body><h1>Page 1</h1><div style='page-break-before: always;'>Page 2</div></body></html>"
        pdf_data = sghtmltopdf.render(html, page_size="A4", orientation="Landscape")
        self.assertTrue(pdf_data.startswith(b"%PDF-"))

    def test_render_with_landscape_bool(self):
        html = "<html><body><h1>Page 1</h1></body></html>"
        pdf_data = sghtmltopdf.render(html, page_size="A4", landscape=True)
        self.assertTrue(pdf_data.startswith(b"%PDF-"))

    def test_render_with_replace(self):
        html = "<html><body><h1>Page 1</h1></body></html>"
        pdf_data = sghtmltopdf.render(
            html,
            header_left="[title]",
            replace={"[title]": "My Document"},
        )
        self.assertTrue(pdf_data.startswith(b"%PDF-"))

    def test_render_bytes_input(self):
        html = b"<html><body><p>Bytes test</p></body></html>"
        pdf_data = sghtmltopdf.render(html)
        self.assertTrue(pdf_data.startswith(b"%PDF-"))

    def test_render_invalid_option(self):
        html = "<html><body><p>test</p></body></html>"
        with self.assertRaises(ValueError):
            sghtmltopdf.render(html, invalid_unknown_option_xyz=True)

    def test_render_threads(self):
        import concurrent.futures

        html = "<html><body><h1>Multithreaded Render</h1></body></html>"
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(sghtmltopdf.render, html, page_size="A4") for _ in range(8)]
            results = [f.result() for f in futures]

        for pdf_data in results:
            self.assertTrue(pdf_data.startswith(b"%PDF-"))
            self.assertGreater(len(pdf_data), 100)


if __name__ == "__main__":
    unittest.main()
