library(gt)
library(tidyverse)
library(glue)


apa_style <- function(tab) {
  tab %>%
    tab_options(
      table.border.top.color = "white",
      heading.title.font.size = px(16),
      column_labels.border.top.width = 3,
      column_labels.border.top.color = "black",
      column_labels.border.bottom.width = 3,
      column_labels.vlines.width = 0,
      table_body.vlines.width = 0,
      summary_row.border.width = 0,
      heading.border.bottom.width = 0,
      grand_summary_row.border.width = 0,
      column_labels.border.bottom.color = "black",
      table_body.border.bottom.color = "black",
      table.border.bottom.color = "white",
      table.width = pct(100),
      table.background.color = "white",
      row_group.border.bottom.color = "white",
      row_group.border.top.color = "white",
      table_body.hlines.color = "white",
      stub.border.width = 0
    ) %>%
    cols_align(align="center") %>%
    tab_style(
      style = list(
        cell_borders(
          sides = c("top", "bottom"),
          color = "white",
          weight = px(1)
        ),
        cell_text(
          align="center"
        ),
        cell_fill(color = "white", alpha = NULL)
      ),
      locations = cells_body(
        columns = everything(),
        rows = everything()
      )
    )
}
