package com.jav.server.controller.base;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;


@Controller
@RequestMapping("index")
public class IndexController {
    @GetMapping
    public ModelAndView index(Model model) {
        return new ModelAndView("index");
    }
    
}
